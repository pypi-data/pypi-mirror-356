#!/usr/bin/env python3
"""
NIfTI to DICOM converter for Orthanc upload
将NIfTI文件转换为DICOM并上传到Orthanc服务器
"""

import os
import sys
import tempfile
import argparse
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional

try:
    import nibabel as nib
    import numpy as np
    import pydicom
    from pydicom.dataset import Dataset, FileDataset
    from pydicom.uid import generate_uid
    import requests
except ImportError as e:
    print(f"❌ 缺少必要的依赖包: {e}")
    print("请运行: pip install nibabel numpy pydicom requests")
    sys.exit(1)


class NiiToDicomConverter:
    """NIfTI到DICOM转换器"""
    
    def __init__(self, orthanc_url: str = "http://localhost:8042"):
        self.orthanc_url = orthanc_url
        self.patient_counter = 1
        
    def create_dicom_from_nii(
        self, 
        nii_path: str, 
        output_dir: str, 
        patient_id: Optional[str] = None, 
        study_description: str = "LITS Challenge"
    ) -> Tuple[List[str], str, str, str]:
        """将NIfTI文件转换为DICOM序列
        
        Args:
            nii_path: NIfTI文件路径
            output_dir: 输出目录
            patient_id: 患者ID（可选）
            study_description: 检查描述
            
        Returns:
            Tuple[DICOM文件列表, 患者ID, Study UID, Series UID]
        """
        
        print(f"📖 读取NIfTI文件: {nii_path}")
        
        # 读取NIfTI文件
        try:
            nii_img = nib.load(nii_path)
            nii_data = nii_img.get_fdata()
            affine = nii_img.affine
            header = nii_img.header
        except Exception as e:
            raise ValueError(f"无法读取NIfTI文件: {e}")
        
        # 获取文件信息
        filename = Path(nii_path).stem
        if filename.endswith('.nii'):
            filename = filename[:-4]  # 移除.nii后缀
            
        is_segmentation = "segmentation" in filename.lower()
        
        # 生成DICOM元数据
        if patient_id is None:
            # 从文件名提取患者信息
            if "volume-" in filename:
                patient_num = filename.split("volume-")[1].split("_")[0]
                patient_id = f"LITS_{patient_num.zfill(3)}"
            elif "test-volume-" in filename:
                patient_num = filename.split("test-volume-")[1].split("_")[0]
                patient_id = f"TEST_{patient_num.zfill(3)}"
            else:
                patient_id = f"LITS_{self.patient_counter:03d}"
                self.patient_counter += 1
            
        study_uid = generate_uid()
        series_uid = generate_uid()
        
        # 处理数据类型和范围
        print(f"📊 原始数据形状: {nii_data.shape}")
        print(f"📊 原始数据范围: {nii_data.min():.2f} ~ {nii_data.max():.2f}")
        
        if is_segmentation:
            # 分割图像：确保是整数标签
            nii_data = np.round(nii_data).astype(np.uint16)
            series_description = f"Segmentation - {filename}"
            modality = "SEG"
            window_center = nii_data.max() // 2
            window_width = int(nii_data.max())
            rescale_intercept = 0
            rescale_slope = 1
        else:
            # CT图像：处理Hounsfield单位
            # NIfTI中的CT值已经是真实的HU单位，保持原始范围
            original_min, original_max = nii_data.min(), nii_data.max()
            print(f"📊 CT值范围: {original_min:.1f} ~ {original_max:.1f} HU")
            
            # 检查数据类型，选择合适的存储方式
            if nii_data.dtype == np.int16:
                # 如果原本是int16，直接使用（可能已经正确处理了）
                nii_data = nii_data.astype(np.int16)
                rescale_intercept = 0
                rescale_slope = 1
            else:
                # 其他情况，确保在有效范围内
                nii_data = np.clip(nii_data, -3024, 3071)  # 扩展CT值范围
                nii_data = nii_data.astype(np.int16)
                rescale_intercept = 0
                rescale_slope = 1
            
            series_description = f"CT Volume - {filename}"
            modality = "CT"
            # 使用适合CT的窗位窗宽
            window_center = 40  # 腹部软组织窗位
            window_width = 400  # 腹部软组织窗宽
        
        print(f"📊 处理后数据范围: {nii_data.min()} ~ {nii_data.max()}")
        
        # 从NIfTI header获取真实的空间信息
        try:
            # 优先使用header中的zooms信息（更准确）
            zooms = header.get_zooms()
            if len(zooms) >= 3:
                pixel_spacing = [float(zooms[0]), float(zooms[1])]
                slice_thickness = float(zooms[2])
            else:
                # 备用方案：从affine矩阵提取
                pixel_spacing = [abs(affine[0, 0]), abs(affine[1, 1])]
                slice_thickness = abs(affine[2, 2])
            
            # 获取空间单位
            units = header.get_xyzt_units()
            spatial_unit = units[0] if units else 'mm'
            
            # 获取图像方向信息
            orientation_matrix = affine[:3, :3]
            # 标准化方向向量
            image_orientation = []
            for i in range(2):  # 只需要前两个方向向量
                col = orientation_matrix[:, i]
                norm = np.linalg.norm(col)
                if norm > 0:
                    normalized = col / norm
                    image_orientation.extend(normalized.tolist())
                else:
                    # 默认方向
                    if i == 0:
                        image_orientation.extend([1.0, 0.0, 0.0])
                    else:
                        image_orientation.extend([0.0, 1.0, 0.0])
            
            # 获取原点位置
            origin = affine[:3, 3]
            
        except Exception as e:
            print(f"⚠️  无法提取空间信息，使用默认值: {e}")
            pixel_spacing = [1.0, 1.0]
            slice_thickness = 1.0
            spatial_unit = 'mm'
            image_orientation = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
            origin = [0.0, 0.0, 0.0]
            
        print(f"📏 像素间距: {pixel_spacing}, 层厚: {slice_thickness}")
        
        dicom_files = []
        
        # 为每个切片创建DICOM文件
        num_slices = nii_data.shape[2]
        print(f"🔄 开始转换 {num_slices} 个切片...")
        
        for slice_idx in range(num_slices):
            if slice_idx % 20 == 0:
                print(f"  处理切片 {slice_idx + 1}/{num_slices}")
                
            slice_data = nii_data[:, :, slice_idx]
            
            # 创建DICOM数据集
            ds = self._create_dicom_dataset(
                slice_data, 
                patient_id, 
                study_uid, 
                series_uid, 
                slice_idx,
                series_description,
                modality,
                study_description,
                pixel_spacing,
                slice_thickness,
                window_center,
                window_width,
                image_orientation,
                origin,
                rescale_intercept,
                rescale_slope
            )
            
            # 保存DICOM文件
            output_file = os.path.join(output_dir, f"{filename}_slice_{slice_idx:04d}.dcm")
            ds.save_as(output_file)
            dicom_files.append(output_file)
            
        print(f"✅ 成功生成 {len(dicom_files)} 个DICOM文件")
        return dicom_files, patient_id, study_uid, series_uid
    
    def _create_dicom_dataset(
        self, 
        slice_data: np.ndarray, 
        patient_id: str, 
        study_uid: str, 
        series_uid: str, 
        slice_idx: int,
        series_description: str, 
        modality: str, 
        study_description: str,
        pixel_spacing: List[float],
        slice_thickness: float,
        window_center: int,
        window_width: int,
        image_orientation: List[float],
        origin: List[float],
        rescale_intercept: float,
        rescale_slope: float
    ) -> FileDataset:
        """创建DICOM数据集"""
        
        # 基本DICOM头信息
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = pydicom.uid.CTImageStorage
        file_meta.MediaStorageSOPInstanceUID = generate_uid()
        file_meta.ImplementationClassUID = generate_uid()
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        
        # 创建数据集
        ds = FileDataset("temp", {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        # 患者信息
        ds.PatientName = f"LITS Patient {patient_id}"
        ds.PatientID = patient_id
        ds.PatientBirthDate = "19800101"
        ds.PatientSex = "U"  # Unknown
        
        # 检查信息
        ds.StudyInstanceUID = study_uid
        ds.StudyDate = datetime.now().strftime("%Y%m%d")
        ds.StudyTime = datetime.now().strftime("%H%M%S")
        ds.StudyDescription = study_description
        ds.AccessionNumber = f"ACC_{patient_id}"
        ds.StudyID = "1"
        
        # 序列信息
        ds.SeriesInstanceUID = series_uid
        ds.SeriesNumber = 1
        ds.SeriesDescription = series_description
        ds.Modality = modality
        ds.SeriesDate = ds.StudyDate
        ds.SeriesTime = ds.StudyTime
        
        # 实例信息
        ds.SOPInstanceUID = generate_uid()
        ds.SOPClassUID = pydicom.uid.CTImageStorage
        ds.InstanceNumber = slice_idx + 1
        ds.ContentDate = ds.StudyDate
        ds.ContentTime = ds.StudyTime
        
        # 图像信息
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = "MONOCHROME2"
        ds.Rows, ds.Columns = slice_data.shape
        
        # 根据数据类型设置位深度
        if slice_data.dtype == np.int16:
            ds.BitsAllocated = 16
            ds.BitsStored = 16
            ds.HighBit = 15
            ds.PixelRepresentation = 1  # 有符号整数
        else:  # uint16 或其他
            ds.BitsAllocated = 16
            ds.BitsStored = 16
            ds.HighBit = 15
            ds.PixelRepresentation = 0  # 无符号整数
        
        # 显示参数
        ds.WindowCenter = str(window_center)
        ds.WindowWidth = str(window_width)
        
        # CT特定信息
        if modality == "CT":
            ds.RescaleIntercept = rescale_intercept
            ds.RescaleSlope = rescale_slope
            ds.Units = "HU"
            ds.KVP = "120"  # 假设120kV
        
        # 使用NIfTI中的真实空间信息
        # 计算每个切片的真实世界坐标位置
        slice_position = [
            float(origin[0]), 
            float(origin[1]), 
            float(origin[2] + slice_idx * slice_thickness)
        ]
        
        ds.ImagePositionPatient = slice_position
        ds.ImageOrientationPatient = [f"{x:.6f}" for x in image_orientation]
        # 修复VR DS长度警告 - 限制精度
        ds.PixelSpacing = [f"{pixel_spacing[0]:.6f}", f"{pixel_spacing[1]:.6f}"]
        ds.SliceThickness = f"{slice_thickness:.6f}"
        ds.SliceLocation = slice_position[2]  # Z坐标作为slice location
        
        # 设置像素数据（保持原始数据类型）
        if slice_data.dtype == np.int16:
            ds.PixelData = slice_data.astype(np.int16).tobytes()
        else:
            ds.PixelData = slice_data.astype(np.uint16).tobytes()
        
        # 确保数据一致性
        ds.fix_meta_info()
        
        return ds
    
    def upload_to_orthanc(self, dicom_file: str) -> Tuple[bool, str]:
        """上传DICOM文件到Orthanc
        
        Args:
            dicom_file: DICOM文件路径
            
        Returns:
            Tuple[成功标志, 结果信息]
        """
        try:
            # 验证DICOM文件是否有效
            file_size = os.path.getsize(dicom_file)
            if file_size == 0:
                return False, "DICOM文件为空"
            
            with open(dicom_file, 'rb') as f:
                # 使用正确的上传方式
                response = requests.post(
                    f"{self.orthanc_url}/instances",
                    data=f.read(),
                    headers={'Content-Type': 'application/dicom'},
                    timeout=30
                )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    return True, f"上传成功: {result.get('ID', 'Unknown ID')}"
                except:
                    # 有时Orthanc返回文本而不是JSON
                    return True, f"上传成功: {response.text[:50]}"
            elif response.status_code == 409:
                return True, "文件已存在 (跳过重复)"
            else:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {response.text[:200]}"
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            return False, "无法连接到Orthanc服务器，请确保服务正在运行"
        except requests.exceptions.Timeout:
            return False, "上传超时"
        except Exception as e:
            return False, f"上传失败: {str(e)}"
    
    def test_orthanc_connection(self) -> bool:
        """测试Orthanc连接"""
        try:
            response = requests.get(f"{self.orthanc_url}/system", timeout=5)
            if response.status_code == 200:
                system_info = response.json()
                print(f"✅ Orthanc连接成功!")
                print(f"   版本: {system_info.get('Version', 'Unknown')}")
                print(f"   名称: {system_info.get('Name', 'Unknown')}")
                return True
            else:
                print(f"❌ Orthanc响应错误: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 无法连接到Orthanc: {e}")
            print(f"   请确保Orthanc服务在 {self.orthanc_url} 运行")
            return False
    
    def convert_and_upload_nii(self, nii_path: str, patient_id: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
        """转换NIfTI文件并上传到Orthanc
        
        Args:
            nii_path: NIfTI文件路径
            patient_id: 可选的患者ID
            
        Returns:
            Tuple[成功标志, 患者ID, Study UID, Series UID]
        """
        print(f"\n🔄 处理文件: {nii_path}")
        
        # 检查文件是否存在
        if not Path(nii_path).exists():
            print(f"❌ 文件不存在: {nii_path}")
            return False, None, None, None
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # 转换为DICOM
                dicom_files, pid, study_uid, series_uid = self.create_dicom_from_nii(
                    nii_path, temp_dir, patient_id
                )
                
                print(f"📋 患者ID: {pid}")
                print(f"📋 Study UID: {study_uid}")
                print(f"📋 Series UID: {series_uid}")
                
                # 上传到Orthanc
                print(f"📤 开始上传到Orthanc...")
                success_count = 0
                failed_count = 0
                
                for i, dcm_file in enumerate(dicom_files):
                    success, result = self.upload_to_orthanc(dcm_file)
                    if success:
                        success_count += 1
                        if (i + 1) % 50 == 0:  # 每50个切片显示一次进度
                            print(f"  📤 已上传 {i+1}/{len(dicom_files)} 切片")
                    else:
                        failed_count += 1
                        if failed_count <= 3:  # 只显示前3个错误
                            print(f"  ❌ 切片 {i+1} 上传失败: {result}")
                
                if success_count == len(dicom_files):
                    print(f"🎉 全部上传成功! ({success_count} 个切片)")
                elif success_count > 0:
                    print(f"⚠️  部分上传成功: {success_count}/{len(dicom_files)} 个切片")
                else:
                    print(f"❌ 上传完全失败")
                    return False, pid, study_uid, series_uid
                
                return True, pid, study_uid, series_uid
                
            except Exception as e:
                print(f"❌ 转换失败: {str(e)}")
                return False, None, None, None


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='将NIfTI文件转换为DICOM并上传到Orthanc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 转换单个文件
  nii-to-dicom volume-0.nii
  
  # 转换目录中的所有文件
  nii-to-dicom dataset/Training_Batch1/
  
  # 指定Orthanc服务器地址
  nii-to-dicom volume-0.nii --orthanc-url http://192.168.1.100:8042
  
  # 指定患者ID
  nii-to-dicom volume-0.nii --patient-id "CUSTOM_001"
        """
    )
    parser.add_argument('input_path', help='NIfTI文件路径或包含NIfTI文件的目录')
    parser.add_argument('--orthanc-url', default='http://localhost:8042', 
                       help='Orthanc服务器URL (默认: http://localhost:8042)')
    parser.add_argument('--patient-id', help='指定患者ID (可选)')
    parser.add_argument('--test-only', action='store_true', 
                       help='仅测试转换，不上传到Orthanc')
    
    args = parser.parse_args()
    
    print("🏥 NIfTI to DICOM 转换器")
    print("=" * 50)
    
    converter = NiiToDicomConverter(args.orthanc_url)
    
    # 测试Orthanc连接 (除非是仅测试模式)
    if not args.test_only and not converter.test_orthanc_connection():
        print("\n💡 提示: 您可以使用 --test-only 标志来仅测试转换功能")
        return
    
    input_path = Path(args.input_path)
    
    if input_path.is_file() and input_path.suffix.lower() in ['.nii', '.gz']:
        # 处理单个文件
        if args.test_only:
            print(f"🧪 测试模式: 仅转换 {input_path}")
            # 在测试模式下，我们仍然可以转换但不上传
        
        success, pid, study_uid, series_uid = converter.convert_and_upload_nii(
            str(input_path), args.patient_id
        )
        
        if success:
            print(f"\n✅ 处理完成!")
            if not args.test_only:
                print(f"🌐 查看结果: {args.orthanc_url}/app/explorer.html")
        
    elif input_path.is_dir():
        # 处理目录中的所有NIfTI文件
        nii_files = []
        for pattern in ['**/*.nii', '**/*.nii.gz']:
            nii_files.extend(list(input_path.glob(pattern)))
        
        if not nii_files:
            print(f"❌ 在 {input_path} 中未找到NIfTI文件")
            return
        
        print(f"🔍 找到 {len(nii_files)} 个NIfTI文件")
        
        success_count = 0
        for i, nii_file in enumerate(nii_files, 1):
            print(f"\n📁 处理文件 {i}/{len(nii_files)}")
            success, pid, study_uid, series_uid = converter.convert_and_upload_nii(str(nii_file))
            if success:
                success_count += 1
            print("-" * 50)
        
        print(f"\n📊 处理完成: {success_count}/{len(nii_files)} 个文件成功")
        if not args.test_only and success_count > 0:
            print(f"🌐 查看结果: {args.orthanc_url}/app/explorer.html")
    
    else:
        print("❌ 输入路径无效，请提供NIfTI文件或包含NIfTI文件的目录")


if __name__ == "__main__":
    main() 