# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 00:33:49 2025

@author: 2
"""

import math
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import pyproj
import math
from typing import List, Tuple, Dict, Optional
import rasterio
import imageio
from osgeo import gdal
import cv2
import time
import pandas as pd
from scipy.interpolate import griddata  # 引入griddata函数
class cehuibaibaoxiang:
    @staticmethod
    def help():
        help_info = """
        cehuibaibaoxiang模块包含以下类：

        1. duanmianjisuan
            - 用途：计算断面面积，包括纵断面和横断面。
            - 用法：调用read_profile_data方法读取数据，然后调用display_results方法展示结果。
            - 示例：
                >>> results = duanmianjisuan.read_profile_data('data.txt')
                >>> duanmianjisuan.display_results(results)

        2. MapSheetCalculator
            - 用途：计算图幅编号，包括旧图幅编号和新图幅编号。
            - 用法：调用calculate_multiple_sheet_numbers方法，传入坐标文件路径和比例尺。
            - 示例：
                >>> MapSheetCalculator.calculate_multiple_sheet_numbers('coordinates.txt', '1:100万')

        3. RANSAC
            - 用途：实现RANSAC算法，用于拟合模型并去除离群点。
            - 用法：创建RANSAC实例，传入点数据和阈值等参数，然后调用fit方法拟合模型。
            - 示例：
                >>> points = RANSAC.read_ransac_data('points.txt')
                >>> ransac = RANSAC(points)
                >>> model, inliers = ransac.fit()
                >>> RANSAC.display_ransac_results(points, model, inliers)

        4. Denoising
            - 用途：对点云数据进行去噪处理。
            - 用法：调用read_point_cloud_data方法读取点云数据，然后调用statistical_outlier_filter方法进行去噪。
            - 示例：
                >>> point_cloud = Denoising.read_point_cloud_data('point_cloud.txt')
                >>> denoised_points = Denoising.statistical_outlier_filter(point_cloud, k=10, alpha=1.5)
                >>> Denoising.display_denoising_results(point_cloud, denoised_points)

        5. BackwardIntersectionsheying
            - 用途：实现后方交会计算。
            - 用法：创建BackwardIntersectionsheying实例，传入控制点、焦距、比例尺和主点坐标，然后调用calculate方法进行计算。
            - 示例：
                >>> control_points = BackwardIntersectionsheying.read_control_points('control_points.txt')
                >>> backward_intersection = BackwardIntersectionsheying(control_points, focal_length=30, scale=0.5, principal_point_x=10, principal_point_y=20)
                >>> result = backward_intersection.calculate()
                >>> BackwardIntersectionsheying.display_backward_intersection_results(result)

        6. VoronoiDiagram
            - 用途：生成泰森多边形。
            - 用法：调用read_voronoi_points方法读取点数据，然后调用generate_voronoi方法生成泰森多边形。
            - 示例：
                >>> points = VoronoiDiagram.read_voronoi_points('voronoi_points.txt')
                >>> voronoi_cells = VoronoiDiagram.generate_voronoi(points, bounds=(0, 1000, 0, 1000))
                >>> VoronoiDiagram.display_voronoi_diagram(voronoi_cells)

        7. InteriorOrientation
            - 用途：计算内定向参数。
            - 用法：调用calculate_interior_orientation方法，传入像框标志和像素标志。
            - 示例：
                >>> frame_marks = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
                >>> pixel_marks = np.array([[0, 0], [10, 0], [0, 10], [10, 10]])
                >>> params, resX, resY = InteriorOrientation.calculate_interior_orientation(frame_marks, pixel_marks)

        8. RelativeOrientation
            - 用途：计算相对定向参数。
            - 用法：调用calculate_relative_orientation方法，传入左右影像点、焦距和基线。
            - 示例：
                >>> left = np.array([[1, 2], [3, 4], [5, 6]])
                >>> right = np.array([[2, 3], [4, 5], [6, 7]])
                >>> params, Q, iter_count = RelativeOrientation.calculate_relative_orientation(left, right, f=30, B=[10])

        9. ForwardIntersection
            - 用途：计算前方交会。
            - 用法：调用calculate_forward_intersection方法，传入左右影像点、相对定向参数、焦距和基线。
            - 示例：
                >>> left = np.array([[1, 2], [3, 4], [5, 6]])
                >>> right = np.array([[2, 3], [4, 5], [6, 7]])
                >>> rel_params = {'phi1': 0, 'omega1': 0, 'kappa1': 0, 'phi2': 0, 'omega2': 0, 'kappa2': 0}
                >>> X, Y, Z, deltaY = ForwardIntersection.calculate_forward_intersection(left, right, rel_params, f=30, B=[10])

        10. AbsoluteOrientation
            - 用途：计算绝对定向参数。
            - 用法：调用calculate_absolute_orientation方法，传入模型点和地面点。
            - 示例：
                >>> model_pts = np.array([[1, 2, 3], [4, 5, 6]])
                >>> ground_pts = np.array([[10, 20, 30], [40, 50, 60]])
                >>> params, residuals = AbsoluteOrientation.calculate_absolute_orientation(model_pts, ground_pts)

        11. ResultOutput
            - 用途：保存结果。
            - 用法：调用save_results方法，传入模型坐标、地面坐标和文件路径。
            - 示例：
                >>> model_coords = np.array([[1, 2, 3], [4, 5, 6]])
                >>> ground_coords = np.array([[10, 20, 30], [40, 50, 60]])
                >>> ResultOutput.save_results(model_coords, ground_coords, 'results.txt')

        12. MagneticFieldCalculator
            - 用途：计算磁场强度。
            - 用法：创建MagneticFieldCalculator实例，然后调用calculate_B方法计算磁场强度。
            - 示例：
                >>> calculator = MagneticFieldCalculator()
                >>> B = calculator.calculate_B(N=3, x=np.linspace(0, 1, 100))
                >>> calculator.plot_B_vs_x(N_values=[3, 4, 5])

        13. ContourGenerator
            - 用途：生成等高线。
            - 用法：创建ContourGenerator实例，传入DEM文件路径和等高线间隔，然后调用generate_contours方法生成等高线。
            - 示例：
                >>> contour_generator = ContourGenerator(dem_file_path='dem.tif', contour_interval=10)
                >>> contour_generator.load_dem_data()
                >>> contour_generator.generate_contours()

        14. DelaunayTriangulator
            - 用途：生成Delaunay三角网。
            - 用法：创建DelaunayTriangulator实例，传入点列表，然后调用triangulate方法生成三角网。
            - 示例：
                >>> points = [(0, 0), (1, 0), (0, 1), (1, 1)]
                >>> triangulator = DelaunayTriangulator(points)
                >>> triangulator.triangulate()
                >>> triangulator.display_triangulation()

        15. DEMGenerator
            - 用途：生成DEM。
            - 用法：创建DEMGenerator实例，传入CSV文件路径、列名和分辨率，然后调用generate_dem方法生成DEM。
            - 示例：
                >>> dem_generator = DEMGenerator(csv_file_path='elevation.csv', x_col='X', y_col='Y', z_col='Z', resolution=200)
                >>> dem_generator.load_csv_data()
                >>> dem_generator.generate_dem()

        16. SlopeCalculator
            - 用途：计算坡度。
            - 用法：创建SlopeCalculator实例，传入DEM文件路径，然后调用calculate_slope方法计算坡度。
            - 示例：
                >>> slope_calculator = SlopeCalculator(dem_file_path='dem.tif')
                >>> slope_calculator.load_dem_data()
                >>> slope_calculator.calculate_slope()

        17. AspectCalculator
            - 用途：计算坡向。
            - 用法：创建AspectCalculator实例，传入DEM文件路径，然后调用calculate_aspect方法计算坡向。
            - 示例：
                >>> aspect_calculator = AspectCalculator(dem_file_path='dem.tif')
                >>> aspect_calculator.load_dem_data()
                >>> aspect_calculator.calculate_aspect()

        18. HarrisCornerDetector
            - 用途：检测角点。
            - 用法：调用detect方法，传入图像路径。
            - 示例：
                >>> detector = HarrisCornerDetector()
                >>> harris_img, dog_img = detector.detect('image.jpg', harris_corners_num=200, harris_thresh=0.04, dog_levels=3)

        19. ImageTransformer
            - 用途：对图像进行变换。
            - 用法：调用transform方法，传入图像路径。
            - 示例：
                >>> transformer = ImageTransformer()
                >>> transformer.transform('image.jpg')

        20. ImageFilter
            - 用途：对图像进行滤波。
            - 用法：调用apply_filter方法，传入图像路径、滤波类型和参数。
            - 示例：
                >>> filter = ImageFilter()
                >>> filter.apply_filter('image.jpg', filter_type='jq', params=[1, 2, 1, 2, 1, 2, 1, 2, 1])

        21. LOGDetector
            - 用途：检测边缘。
            - 用法：调用detect方法，传入图像路径。
            - 示例：
                >>> detector = LOGDetector()
                >>> edge = detector.detect('image.jpg', cd=9)

        22. HistogramCalculator
            - 用途：计算并绘制直方图。
            - 用法：调用calculate_and_draw方法，传入图像路径。
            - 示例：
                >>> calculator = HistogramCalculator()
                >>> hist_image = calculator.calculate_and_draw('image.jpg')

        23. PerformanceComparator
            - 用途：比较算法性能。
            - 用法：调用compare方法，传入图像路径。
            - 示例：
                >>> comparator = PerformanceComparator()
                >>> comparator.compare('image.jpg', n=9)

        24. GaussForward
            - 用途：高斯正算。
            - 用法：创建GaussForward实例，传入经纬度、距离和方位角，然后调用forward_gauss方法进行计算。
            - 示例：
                >>> gauss_forward = GaussForward(B1=30, L1=120, s12=1000, A12=45)
                >>> x, y = gauss_forward.forward_gauss()

        25. GaussInverse
            - 用途：高斯反算。
            - 用法：创建GaussInverse实例，传入经纬度和坐标，然后调用inverse_gauss方法进行计算。
            - 示例：
                >>> gauss_inverse = GaussInverse(B1=30, L1=120, x=1000, y=2000)
                >>> B1p, L1p, s12p, A12p = gauss_inverse.inverse_gauss()

        26. SideIntersection
            - 用途：测边交会。
            - 用法：创建SiSideIntersection实例，传入点坐标和距离，然后调用calculate方法进行计算。
            - 示例：
                >>> side_intersection = SideIntersection(x1=0, y1=0, x2=100, y2=100, sa=100, sb=100)
                >>> xp, yp = side_intersection.calculate()

        27. AngleIntersection
            - 用途：测角交会。
            - 用法：创建AngleIntersection实例，传入点坐标和角度，然后调用calculate方法进行计算。
            - 示例：
                >>> angle_intersection = AngleIntersection(x1=0, y1=0, x2=100, y2=100, a=45, b=45)
                >>> xp, yp = angle_intersection.calculate()

        28. SideAngleIntersection
            - 用途：边角交会。
            - 用法：创建SideAngleIntersection实例，传入点坐标和角度，然后调用calculate方法进行计算。
            - 示例：
                >>> side_angle_intersection = SideAngleIntersection(x1=0, y1=0, x2=100, y2=100, jcg=90)
                >>> xp, yp = side_angle_intersection.calculate()

        29. BackwardIntersectionceliangxue
            - 用途：后方交会测量学。
            - 用法：创建BackwardIntersectionceliangxue实例，传入角度和点坐标，然后调用calculate方法进行计算。
            - 示例：
                >>> backward_celiangxue = BackwardIntersectionceliangxue(ra=30, rb=30, xa=0, xb=100, xc=50, ya=0, yb=0, yc=50)
                >>> xp, yp = backward_celiangxue.calculate()

        30. EightParameterTransformation
            - 用途：七参数变换。
            - 用法：创建EightParameterTransformation实例，传入Excel文件路径，然后调用find_parameter等方法。
            - 示例：
                >>> transformation = EightParameterTransformation(file_path='data.xlsx')
                >>> transformation.find_parameter()
                >>> transformation.check()
                >>> transformed_coords = transformation.transform_coordinates(check_points=[[1, 2], [3, 4]])
                >>> transformation.plot_transformed_points(transformed_coords)
        """
        print(help_info)

# 调用帮助函数
print(cehuibaibaoxiang.help())

class duanmianjisuan:
    @staticmethod
    def read_profile_data(file_path: str) -> Dict:
        """从文件读取断面计算所需的数据"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) < 3:
                    print("文件内容不足，至少需要3行数据！")
                    return None

                reference_point = {'name': lines[0].split(',')[0], 'elevation': float(lines[0].split(',')[1])}
                key_points = lines[1].strip().split(',')

                if len(key_points) < 2:
                    print("关键点行格式不正确！")
                    return None

                data_points = []
                for line in lines[2:]:
                    parts = line.strip().split(',')
                    if len(parts) < 4:
                        print(f"警告：行格式不正确，已跳过: {line.strip()}")
                        continue
                    try:
                        data_points.append({
                            'name': parts[0],
                            'x': float(parts[1]),
                            'y': float(parts[2]),
                            'elevation': float(parts[3])
                        })
                    except ValueError:
                        print(f"警告：行格式不正确，已跳过: {line.strip()}")
                        continue

                if len(data_points) < 2:
                    print("数据点不足，无法进行剖面计算！")
                    return None

                # 查找关键点 A 和 B
                point_a = next((p for p in data_points if p['name'] == key_points[0]), None)
                point_b = next((p for p in data_points if p['name'] == key_points[1]), None)

                if not point_a or not point_b:
                    print(f"错误：未找到关键点 {key_points[0]} 或 {key_points[1]}！")
                    return None

                # 计算纵断面和横断面
                interpolated_points_ab = duanmianjisuan.interpolate_points(point_a, point_b, 2, data_points)
                mid_point = {
                    'x': (point_a['x'] + point_b['x']) / 2,
                    'y': (point_a['y'] + point_b['y']) / 2
                }
                perpendicular_angle = duanmianjisuan.calculate_bearing(point_a['x'], point_a['y'], point_b['x'], point_b['y']) + 90
                interpolated_points_perpendicular = duanmianjisuan.interpolate_perpendicular_section(mid_point, perpendicular_angle, 30, 2, data_points)

                # 计算面积
                total_area_ab = duanmianjisuan.calculate_trapezoidal_area(interpolated_points_ab, reference_point['elevation'])
                total_area_perpendicular = duanmianjisuan.calculate_trapezoidal_area(interpolated_points_perpendicular, reference_point['elevation'])

                return {
                    'reference_point': reference_point,
                    'key_points': key_points,
                    'data_points': data_points,
                    'interpolated_points_ab': interpolated_points_ab,
                    'total_area_ab': total_area_ab,
                    'interpolated_points_perpendicular': interpolated_points_perpendicular,
                    'total_area_perpendicular': total_area_perpendicular
                }
        except Exception as e:
            print(f"Error reading profile data: {e}")
            return None

    @staticmethod
    def interpolate_perpendicular_section(mid_point: Dict[str, float], angle: float, extend_distance: float, interval: float, data_points: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """在中点处做垂线内插点并计算高程"""
        total_extend_distance = 2 * extend_distance
        num_points = int(total_extend_distance / interval)
        interpolated_points = []

        for i in range(-num_points // 2, num_points // 2 + 1):
            distance = i * interval
            radians = math.radians(angle)
            x = mid_point['x'] + distance * math.cos(radians)
            y = mid_point['y'] + distance * math.sin(radians)
            elevation = duanmianjisuan.idw_interpolation({'x': x, 'y': y}, data_points)
            interpolated_points.append({
                'name': f'N{i + num_points // 2}',
                'x': x,
                'y': y,
                'elevation': elevation
            })

        return interpolated_points

    
    @staticmethod
    def calculate_bearing(x1: float, y1: float, x2: float, y2: float) -> float:
        """计算两点之间的方位角（度）"""
        dx = x2 - x1
        dy = y2 - y1
        bearing = math.degrees(math.atan2(dy, dx))
        if dx > 0 and dy > 0:
            return bearing
        elif dx < 0 and dy > 0:
            return 180 + bearing
        elif dx < 0 and dy < 0:
            return 180 + bearing
        elif dx > 0 and dy < 0:
            return 360 + bearing
        elif dx == 0 and dy > 0:
            return 90
        elif dx == 0 and dy < 0:
            return 270
        else:
            return 0

    @staticmethod
    def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
        """计算两点之间的平面距离"""
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx ** 2 + dy ** 2)

    @staticmethod
    def interpolate_points(point_a: Dict, point_b: Dict, interval: float, data_points: List[Dict]) -> List[Dict]:
        """在AB线上内插点并计算高程"""
        total_distance = duanmianjisuan.calculate_distance(point_a['x'], point_a['y'], point_b['x'], point_b['y'])
        if total_distance == 0:
            return []
        num_points = int(total_distance / interval)
        interpolated_points = []
        for i in range(num_points + 1):
            t = i / num_points
            x = point_a['x'] + t * (point_b['x'] - point_a['x'])
            y = point_a['y'] + t * (point_b['y'] - point_a['y'])
            elevation = duanmianjisuan.idw_interpolation({'x': x, 'y': y}, data_points)
            interpolated_points.append({
                'name': f'Z{i}',
                'x': x,
                'y': y,
                'elevation': elevation
            })
        return interpolated_points

    @staticmethod
    def idw_interpolation(target_point: Dict, data_points: List[Dict], power: float = 2.0) -> float:
        """使用IDW方法计算目标点的高程"""
        numerator = 0.0
        denominator = 0.0
        for point in data_points:
            distance = math.sqrt((target_point['x'] - point['x']) ** 2 + (target_point['y'] - point['y']) ** 2)
            if distance == 0:
                return point['elevation']
            weight = 1.0 / (distance ** power)
            numerator += point['elevation'] * weight
            denominator += weight
        return numerator / denominator

    @staticmethod
    def calculate_trapezoidal_area(points: List[Dict], reference_elevation: float) -> float:
        """使用梯形法则计算面积"""
        total_area = 0.0
        for i in range(len(points) - 1):
            base1 = points[i]['elevation'] - reference_elevation
            base2 = points[i + 1]['elevation'] - reference_elevation
            height = duanmianjisuan.calculate_distance(points[i]['x'], points[i]['y'], points[i + 1]['x'], points[i + 1]['y'])
            area = (base1 + base2) * height / 2
            total_area += area
        return total_area

    @staticmethod
    def read_profile_data(file_path: str) -> Dict:
        """从文件读取断面计算所需的数据"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) < 3:
                    print("文件内容不足，至少需要3行数据！")
                    return None

                reference_point = {'name': lines[0].split(',')[0], 'elevation': float(lines[0].split(',')[1])}
                key_points = lines[1].strip().split(',')

                if len(key_points) < 2:
                    print("关键点行格式不正确！")
                    return None

                data_points = []
                for line in lines[2:]:
                    parts = line.strip().split(',')
                    if len(parts) < 4:
                        print(f"警告：行格式不正确，已跳过: {line.strip()}")
                        continue
                    try:
                        data_points.append({
                            'name': parts[0],
                            'x': float(parts[1]),
                            'y': float(parts[2]),
                            'elevation': float(parts[3])
                        })
                    except ValueError:
                        print(f"警告：数据转换错误，已跳过: {line.strip()}")
                        continue

                if len(data_points) < 2:
                    print("数据点不足，无法进行剖面计算！")
                    return None

                # 查找关键点 A 和 B
                point_a = next((p for p in data_points if p['name'] == key_points[0]), None)
                point_b = next((p for p in data_points if p['name'] == key_points[1]), None)

                if not point_a or not point_b:
                    print(f"错误：未找到关键点 {key_points[0]} 或 {key_points[1]}！")
                    return None

                # 计算纵断面和横断面
                interpolated_points_ab = duanmianjisuan.interpolate_points(point_a, point_b, 2, data_points)
                mid_point = {
                    'x': (point_a['x'] + point_b['x']) / 2,
                    'y': (point_a['y'] + point_b['y']) / 2
                }
                angle_ab = duanmianjisuan.calculate_bearing(point_a['x'], point_a['y'], point_b['x'], point_b['y'])
                interpolated_points_perpendicular = duanmianjisuan.interpolate_perpendicular_section(mid_point, angle_ab + 90, 30, 2, data_points)

                # 计算面积
                total_area_ab = duanmianjisuan.calculate_trapezoidal_area(interpolated_points_ab, reference_point['elevation'])
                total_area_perpendicular = duanmianjisuan.calculate_trapezoidal_area(interpolated_points_perpendicular, reference_point['elevation'])

                return {
                    'reference_point': reference_point,
                    'key_points': key_points,
                    'data_points': data_points,
                    'interpolated_points_ab': interpolated_points_ab,
                    'total_area_ab': total_area_ab,
                    'interpolated_points_perpendicular': interpolated_points_perpendicular,
                    'total_area_perpendicular': total_area_perpendicular
                }
        except Exception as e:
            print(f"Error reading profile data: {e}")
            return None


    @staticmethod
    def display_results(results: Dict):
        """展示剖面计算结果"""
        # 展示纵断面
        plt.figure(figsize=(10, 6))
        for point in results['interpolated_points_ab']:
            plt.plot(point['x'], point['elevation'], 'bo')
        plt.xlabel('X Coordinate')
        plt.ylabel('Elevation')
        plt.title(f'Longitudinal Section (Area: {results["total_area_ab"]:.2f})')
        plt.grid(True)
        plt.show()

        # 展示横断面
        plt.figure(figsize=(10, 6))
        for point in results['interpolated_points_perpendicular']:
            plt.plot(point['x'], point['elevation'], 'ro')
        plt.xlabel('X Coordinate')
        plt.ylabel('Elevation')
        plt.title(f'Transverse Section (Area: {results["total_area_perpendicular"]:.2f})')
        plt.grid(True)
        plt.show()

        # 打印详细结果
        print(f"Reference Elevation: {results['reference_point']['elevation']}")
        print(f"Key Points: {', '.join(results['key_points'])}")
        print("\nLongitudinal Section Points:")
        for point in results['interpolated_points_ab']:
            print(f"Point {point['name']}: X={point['x']}, Y={point['y']}, Elevation={point['elevation']}")
        print(f"Total Longitudinal Area: {results['total_area_ab']:.2f}")

        print("\nTransverse Section Points:")
        for point in results['interpolated_points_perpendicular']:
            print(f"Point {point['name']}: X={point['x']}, Y={point['y']}, Elevation={point['elevation']}")
        print(f"Total Transverse Area: {results['total_area_perpendicular']:.2f}")




class MapSheetCalculator:
    @staticmethod
    def calculate_multiple_sheet_numbers(file_path: str, scale: str) -> None:
        """批量计算图幅编号"""
        coordinates = MapSheetCalculator.read_multiple_coordinates(file_path)
        if not coordinates:
            print("未读取到任何有效坐标！")
            return

        results = []
        for lat, lon in coordinates:
            old_sheet = MapSheetCalculator.calculate_old_sheet_number(lon, lat, scale)
            new_sheet = MapSheetCalculator.calculate_new_sheet_number(lon, lat, scale)
            results.append({
                'latitude': lat,
                'longitude': lon,
                'old_sheet': old_sheet[0],
                'new_sheet': new_sheet[0]
            })

        # 打印结果
        print("Batch Calculation Results:")
        print(f"Scale: {scale}")
        for result in results:
            print(f"Latitude: {result['latitude']}, Longitude: {result['longitude']}")
            print(f"Old Sheet Number: {result['old_sheet']}")
            print(f"New Sheet Number: {result['new_sheet']}")
            print("------------------------")

    @staticmethod
    def read_multiple_coordinates(file_path: str) -> List[Tuple[float, float]]:
        """从文件读取多个经纬度坐标"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                coordinates = []
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) != 2:
                        print(f"警告：行格式不正确，已跳过: {line.strip()}")
                        continue
                    try:
                        coordinates.append((float(parts[0]), float(parts[1])))
                    except ValueError:
                        print(f"警告：数据转换错误，已跳过: {line.strip()}")
                        continue
                return coordinates
        except Exception as e:
            print(f"Error reading multiple coordinates: {e}")
            return []

    @staticmethod
    def calculate_old_sheet_number(latitude: float, longitude: float, scale: str) -> List[str]:
        """计算旧图幅编号"""
        row = int(latitude / 4) + 1
        col = int(longitude / 6) + 31
        base_sheet = f"{chr(ord('A') + row - 1)}{col:02d}"
        return MapSheetCalculator._get_subdivisions_old(latitude, longitude, scale, base_sheet)

    @staticmethod
    def calculate_new_sheet_number(latitude: float, longitude: float, scale: str) -> List[str]:
        """计算新图幅编号"""
        row = int(latitude / 4) + 1
        col = int(longitude / 6) + 31
        base_sheet = f"{chr(ord('A') + row - 1)}{col:02d}"
        return MapSheetCalculator._get_subdivisions_new(latitude, longitude, scale, base_sheet)

    @staticmethod
    def _get_subdivisions_old(latitude: float, longitude: float, scale: str, base_sheet: str) -> List[str]:
        """获取旧图幅编号的细分"""
        if scale == "1:100万":
            return [base_sheet]
        elif scale == "1:50万":
            sub_row = int((latitude % 4) / 2)
            sub_col = int((longitude % 6) / 3)
            return [f"{base_sheet}{sub_row * 3 + sub_col + 1}"]
        elif scale == "1:25万":
            sub_row = int((latitude % 4) / 1)
            sub_col = int((longitude % 6) / 1.5)
            return [f"{base_sheet}{sub_row * 4 + sub_col + 1:02d}"]
        elif scale == "1:10万":
            sub_row = int((latitude % 4) / 0.3333)
            sub_col = int((longitude % 6) / 0.5)
            return [f"{base_sheet}{sub_row * 12 + sub_col + 1:03d}"]
        elif scale == "1:5万":
            sub_row = int((latitude % 4) / 0.1667)
            sub_col = int((longitude % 6) / 0.25)
            base_number = sub_row * 24 + sub_col + 1
            quad_number = (sub_row % 2) * 2 + (sub_col % 2) + 1
            return [f"{base_sheet}{base_number:03d}{quad_number}"]
        elif scale == "1:2.5万":
            sub_row = int((latitude % 4) / 0.0833)
            sub_col = int((longitude % 6) / 0.125)
            base_number = sub_row * 48 + sub_col + 1
            quad_number = (sub_row % 2) * 2 + (sub_col % 2) + 1
            return [f"{base_sheet}{base_number:03d}{quad_number}{quad_number}"]
        elif scale == "1:1万":
            sub_row = int((latitude % 4) / 0.0417)
            sub_col = int((longitude % 6) / 0.0625)
            base_number = sub_row * 96 + sub_col + 1
            grid_row = sub_row % 8
            grid_col = sub_col % 8
            grid_number = grid_row * 8 + grid_col + 1
            return [f"{base_sheet}{base_number:03d}{grid_number:02d}"]
        else:
            return [base_sheet]

    @staticmethod
    def _get_subdivisions_new(latitude: float, longitude: float, scale: str, base_sheet: str) -> List[str]:
        """获取新图幅编号的细分"""
        if scale == "1:100万":
            return [base_sheet]
        elif scale == "1:50万":
            sub_row = int((latitude % 4) / 2)
            sub_col = int((longitude % 6) / 3)
            return [f"{base_sheet}B{sub_row:03d}{sub_col:03d}"]
        elif scale == "1:25万":
            sub_row = int((latitude % 4) / 1)
            sub_col = int((longitude % 6) / 1.5)
            return [f"{base_sheet}C{sub_row:03d}{sub_col:03d}"]
        elif scale == "1:10万":
            sub_row = int((latitude % 4) / 0.3333)
            sub_col = int((longitude % 6) / 0.5)
            return [f"{base_sheet}D{sub_row:03d}{sub_col:03d}"]
        elif scale == "1:5万":
            sub_row = int((latitude % 4) / 0.1667)
            sub_col = int((longitude % 6) / 0.25)
            return [f"{base_sheet}E{sub_row:03d}{sub_col:03d}"]
        elif scale == "1:2.5万":
            sub_row = int((latitude % 4) / 0.0833)
            sub_col = int((longitude % 6) / 0.125)
            return [f"{base_sheet}F{sub_row:03d}{sub_col:03d}"]
        elif scale == "1:1万":
            sub_row = int((latitude % 4) / 0.0417)
            sub_col = int((longitude % 6) / 0.0625)
            return [f"{base_sheet}G{sub_row:03d}{sub_col:03d}"]
        else:
            return [base_sheet]


class RANSAC:
    def __init__(self, points: List[Tuple[float, float]], threshold: float = 0.5, probability: float = 0.99, max_iterations: int = 1000):
        self.points = np.array(points)
        self.threshold = threshold
        self.probability = probability
        self.max_iterations = max_iterations
        self.best_model = None
        self.best_inliers = None

    def fit(self):
        best_inliers = []
        best_model = None
        iterations = 0

        while iterations < self.max_iterations:
            sample = self.points[np.random.choice(self.points.shape[0], 2, replace=False)]
            x1, y1 = sample[0]
            x2, y2 = sample[1]

            # 计算直线参数 A, B, C (Ax + By + C = 0)
            A = y2 - y1
            B = x1 - x2
            C = x2 * y1 - x1 * y2

            # 计算内点
            distances = np.abs(A * self.points[:, 0] + B * self.points[:, 1] + C) / np.sqrt(A**2 + B**2)
            inliers = self.points[distances < self.threshold]

            if len(inliers) > len(best_inliers):
                best_inliers = inliers
                best_model = (A, B, C)

                # 更新最大迭代次数
                inlier_ratio = len(best_inliers) / len(self.points)
                self.max_iterations = int(np.log(1 - self.probability) / np.log(1 - inlier_ratio**2))

            iterations += 1

        self.best_model = best_model
        self.best_inliers = best_inliers
        return best_model, best_inliers
    @staticmethod
    def read_ransac_data(file_path: str) -> List[Tuple[float, float]]:
        """从文件读取 RANSAC 算法所需的数据"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                points = []
                for line in lines:
                    parts = line.strip().split()
                    points.append((float(parts[0]), float(parts[1])))
                return points
        except Exception as e:
            print(f"Error reading RANSAC data: {e}")
            return []

    @staticmethod
    def display_ransac_results(points: List[Tuple[float, float]], model: Tuple[float, float, float], inliers: List[Tuple[float, float]]):
        """展示 RANSAC 算法结果"""
        plt.figure(figsize=(10, 6))
        plt.scatter([p[0] for p in points], [p[1] for p in points], c='blue', label='All Points')
        plt.scatter([p[0] for p in inliers], [p[1] for p in inliers], c='red', label='Inliers')
        A, B, C = model
        x_vals = np.linspace(min([p[0] for p in points]), max([p[0] for p in points]), 100)
        y_vals = [(-A * x - C) / B for x in x_vals]
        plt.plot(x_vals, y_vals, 'black', label='Fitted Line')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('RANSAC Results')
        plt.legend()
        plt.grid(True)
        plt.show()


class Denoising:
    @staticmethod
    def read_point_cloud_data(file_path: str) -> List[Dict[str, float]]:
        """从文件读取点云数据"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                point_cloud = []
                for i, line in enumerate(lines):
                    parts = line.strip().split()
                    point_cloud.append({
                        'x': float(parts[0]),
                        'y': float(parts[1]),
                        'z': float(parts[2])
                    })
                return point_cloud
        except Exception as e:
            print(f"Error reading point cloud data: {e}")
            return []

    @staticmethod
    def display_denoising_results(original_points: List[Dict[str, float]], denoised_points: List[Dict[str, float]]):
        """展示去噪结果"""
        original_coords = [[p['x'], p['y'], p['z']] for p in original_points]
        denoised_coords = [[p['x'], p['y'], p['z']] for p in denoised_points]

        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.scatter([p[0] for p in original_coords], [p[1] for p in original_coords], [p[2] for p in original_coords], c='blue', marker='o')
        ax1.set_title('Original Point Cloud')

        ax2 = fig.add_subplot(122, projection='3d')
        ax2.scatter([p[0] for p in denoised_coords], [p[1] for p in denoised_coords], [p[2] for p in denoised_coords], c='red', marker='o')
        ax2.set_title('Denoised Point Cloud')

        plt.show()
    @staticmethod
    def statistical_outlier_filter(point_cloud: List[Dict[str, float]], k: int, alpha: float) -> List[Dict[str, float]]:
        """基于统计的点云去噪"""
        for point in point_cloud:
            neighbors = Denoising._find_k_nearest_neighbors(point, point_cloud, k)
            point['mean_distance'] = Denoising._calculate_mean_distance(point, neighbors)

        mean_distance_all = [p['mean_distance'] for p in point_cloud]
        mean = np.mean(mean_distance_all)
        std_dev = np.std(mean_distance_all)

        denoised_points = []
        for point in point_cloud:
            if point['mean_distance'] < mean + alpha * std_dev:
                denoised_points.append(point)
        return denoised_points

    @staticmethod
    def _find_k_nearest_neighbors(target_point: Dict[str, float], point_cloud: List[Dict[str, float]], k: int) -> List[Dict[str, float]]:
        """查找最近的k个邻点"""
        distances = []
        for point in point_cloud:
            if point != target_point:
                distance = math.sqrt(
                    (target_point['x'] - point['x'])**2 +
                    (target_point['y'] - point['y'])**2 +
                    (target_point['z'] - point['z'])**2
                )
                distances.append((point, distance))
        distances.sort(key=lambda x: x[1])
        return [p[0] for p in distances[:k]]

    @staticmethod
    def _calculate_mean_distance(point: Dict[str, float], neighbors: List[Dict[str, float]]) -> float:
        """计算平均距离"""
        total_distance = 0.0
        for neighbor in neighbors:
            total_distance += math.sqrt(
                (point['x'] - neighbor['x'])**2 +
                (point['y'] - neighbor['y'])**2 +
                (point['z'] - neighbor['z'])**2
            )
        return total_distance / len(neighbors)


class BackwardIntersectionsheying:
    def __init__(self, control_points: List[Dict[str, float]], focal_length: float, scale: float, principal_point_x: float, principal_point_y: float):
        self.control_points = control_points
        self.focal_length = focal_length
        self.scale = scale
        self.principal_point_x = principal_point_x
        self.principal_point_y = principal_point_y
    @staticmethod
    def read_control_points(file_path: str) -> List[Dict[str, float]]:
        """从文件读取后方交会所需的数据"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                control_points = []
                for line in lines:
                    parts = line.strip().split()
                    control_points.append({
                        'x': float(parts[0]),
                        'y': float(parts[1]),
                        'X': float(parts[2]),
                        'Y': float(parts[3]),
                        'Z': float(parts[4])
                    })
                return control_points
        except Exception as e:
            print(f"Error reading control points: {e}")
            return []

    @staticmethod
    def display_backward_intersection_results(result: Dict):
        """展示后方交会计算结果"""
        print(f"Xs: {result['Xs']}")
        print(f"Ys: {result['Ys']}")
        print(f"Zs: {result['Zs']}")
        print(f"Phi: {result['Phi']}")
        print(f"Omega: {result['Omega']}")
        print(f"Kappa: {result['Kappa']}")
        print(f"Iterations: {result['Iterations']}")
        print("Rotation Matrix:")
        print(result['RMatrix'])

    def check_colinear(self) -> bool:
        """检查控制点是否共线（修正后的版本）"""
        if len(self.control_points) < 3:
            return False

        # 获取第一个点的坐标
        x0 = self.control_points[0]['X']
        y0 = self.control_points[0]['Y']
        z0 = self.control_points[0]['Z']

        for i in range(1, len(self.control_points)):
            xi = self.control_points[i]['X']
            yi = self.control_points[i]['Y']
            zi = self.control_points[i]['Z']

            # 计算向量
            dx = xi - x0
            dy = yi - y0
            dz = zi - z0

            # 检查所有后续点是否与第一个点共线
            is_colinear = True
            for j in range(i + 1, len(self.control_points)):
                xj = self.control_points[j]['X']
                yj = self.control_points[j]['Y']
                zj = self.control_points[j]['Z']

                # 计算向量的叉积
                cross_product = dx * (yj - yi) - dy * (xj - xi)
                if abs(cross_product) > 1e-6:
                    is_colinear = False
                    break

            if not is_colinear:
                return False

        return True

    def calculate(self, initial_guess: Optional[List[float]] = None) -> Dict[str, float]:
        """执行后方交会计算"""
        if self.check_colinear():
            raise ValueError("控制点共线，无法进行后方交会计算")

        Xtp = np.array([p['X'] for p in self.control_points])
        Ytp = np.array([p['Y'] for p in self.control_points])
        Ztp = np.array([p['Z'] for p in self.control_points])
        x = np.array([p['x'] for p in self.control_points])
        y = np.array([p['y'] for p in self.control_points])

        m = self.scale
        H = (1 / m) * self.focal_length + np.mean(Ztp)
        Xs0 = np.mean(Xtp)
        Ys0 = np.mean(Ytp)
        Zs0 = H
        phi0 = 0
        omega0 = 0
        kappa0 = 0

        if initial_guess:
            Xs0, Ys0, Zs0, phi0, omega0, kappa0 = initial_guess

        iterations = 0
        tol_Xs = 1
        tol_Ys = 1
        tol_Zs = 1
        tol_phi = 1e-3
        tol_omega = 1e-3
        tol_kappa = 1e-3

        while True:
            iterations += 1

            # 旋转矩阵 R
            a1 = math.cos(phi0) * math.cos(kappa0) - math.sin(phi0) * math.sin(omega0) * math.sin(kappa0)
            a2 = -math.cos(phi0) * math.sin(kappa0) - math.sin(phi0) * math.sin(omega0) * math.cos(kappa0)
            a3 = -math.sin(phi0) * math.cos(omega0)
            b1 = math.cos(omega0) * math.sin(kappa0)
            b2 = math.cos(omega0) * math.cos(kappa0)
            b3 = -math.sin(omega0)
            c1 = math.sin(phi0) * math.cos(kappa0) + math.cos(phi0) * math.sin(omega0) * math.sin(kappa0)
            c2 = -math.sin(phi0) * math.sin(kappa0) + math.cos(phi0) * math.sin(omega0) * math.cos(kappa0)
            c3 = math.cos(phi0) * math.cos(omega0)

            # 计算像点坐标
            calculatedX = []
            calculatedY = []
            for i in range(len(x)):
                Zba = a3 * (Xtp[i] - Xs0) + b3 * (Ytp[i] - Ys0) + c3 * (Ztp[i] - Zs0)
                calculatedX.append(-self.focal_length * (a1 * (Xtp[i] - Xs0) + b1 * (Ytp[i] - Ys0) + c1 * (Ztp[i] - Zs0)) / Zba)
                calculatedY.append(-self.focal_length * (a2 * (Xtp[i] - Xs0) + b2 * (Ytp[i] - Ys0) + c2 * (Ztp[i] - Zs0)) / Zba)

            # 构建误方矩阵 A 和向量 l
            A = []
            l = []
            for i in range(len(x)):
                xi = x[i]
                yi = y[i]
                xa = calculatedX[i]
                ya = calculatedY[i]

                Zba = a3 * (Xtp[i] - Xs0) + b3 * (Ytp[i] - Ys0) + c3 * (Ztp[i] - Zs0)

                a11 = (a1 * self.focal_length + a3 * xi) / Zba
                a12 = (b1 * self.focal_length + b3 * xi) / Zba
                a13 = (c1 * self.focal_length + c3 * xi) / Zba
                a14 = yi * math.sin(omega0) - (xi * (xi * math.cos(kappa0) - yi * math.sin(kappa0)) / self.focal_length + self.focal_length * math.cos(kappa0)) * math.cos(omega0)
                a15 = -self.focal_length * math.sin(kappa0) - xi * (xi * math.sin(kappa0) + yi * math.cos(kappa0)) / self.focal_length
                a16 = yi

                a21 = (a2 * self.focal_length + a3 * yi) / Zba
                a22 = (b2 * self.focal_length + b3 * yi) / Zba
                a23 = (c2 * self.focal_length + c3 * yi) / Zba
                a24 = -xi * math.sin(omega0) - (yi * (xi * math.cos(kappa0) - yi * math.sin(kappa0)) / self.focal_length - self.focal_length * math.sin(kappa0)) * math.cos(omega0)
                a25 = -self.focal_length * math.cos(kappa0) - yi * (xi * math.sin(kappa0) + yi * math.cos(kappa0)) / self.focal_length
                a26 = -xi

                lx = xi - xa
                ly = yi - ya

                A.append([a11, a12, a13, a14, a15, a16])
                A.append([a21, a22, a23, a24, a25, a26])
                l.append(lx)
                l.append(ly)

            A = np.array(A)
            l = np.array(l)

            # 计算 ATA = A^T * A 和 ATl = A^T * l
            ATA = A.T @ A
            ATl = A.T @ l

            # 计算 delta = ATA^-1 * ATl
            try:
                ATA_inv = np.linalg.inv(ATA)
                delta = ATA_inv @ ATl
            except np.linalg.LinAlgError:
                break

            # 更新外方位元素
            Xs0 += delta[0]
            Ys0 += delta[1]
            Zs0 += delta[2]
            phi0 += delta[3]
            omega0 += delta[4]
            kappa0 += delta[5]

            # 检查收敛条件
            if (abs(delta[0]) < tol_Xs and abs(delta[1]) < tol_Ys and abs(delta[2]) < tol_Zs and
                abs(delta[3]) < tol_phi and abs(delta[4]) < tol_omega and abs(delta[5]) < tol_kappa):
                break

        # 计算旋转矩阵 R
        a1_rot = math.cos(phi0) * math.cos(kappa0) - math.sin(phi0) * math.sin(omega0) * math.sin(kappa0)
        a2_rot = -math.cos(phi0) * math.sin(kappa0) - math.sin(phi0) * math.sin(omega0) * math.cos(kappa0)
        a3_rot = -math.sin(phi0) * math.cos(omega0)
        b1_rot = math.cos(omega0) * math.sin(kappa0)
        b2_rot = math.cos(omega0) * math.cos(kappa0)
        b3_rot = -math.sin(omega0)
        c1_rot = math.sin(phi0) * math.cos(kappa0) + math.cos(phi0) * math.sin(omega0) * math.sin(kappa0)
        c2_rot = -math.sin(phi0) * math.sin(kappa0) + math.cos(phi0) * math.sin(omega0) * math.cos(kappa0)
        c3_rot = math.cos(phi0) * math.cos(omega0)

        R_matrix = np.array([
            [a1_rot, a2_rot, a3_rot],
            [b1_rot, b2_rot, b3_rot],
            [c1_rot, c2_rot, c3_rot]
        ])

        return {
            'Xs': Xs0,
            'Ys': Ys0,
            'Zs': Zs0,
            'Phi': phi0,
            'Omega': omega0,
            'Kappa': kappa0,
            'Iterations': iterations,
            'RMatrix': R_matrix
        }

class VoronoiDiagram:
    @staticmethod
    def read_voronoi_points(file_path: str) -> List[Tuple[float, float]]:
        """从文件读取泰森多边形所需的数据"""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                points = []
                for line in lines:
                    parts = line.strip().split(',')
                    points.append((float(parts[0]), float(parts[1])))
                return points
        except Exception as e:
            print(f"Error reading Voronoi points: {e}")
            return []

    @staticmethod
    def display_voronoi_diagram(voronoi_cells: List[Dict]):
        """展示泰森多边形结果"""
        plt.figure(figsize=(10, 8))
        for cell in voronoi_cells:
            x = [vertex[0] for vertex in cell['vertices']]
            y = [vertex[1] for vertex in cell['vertices']]
            plt.fill(x, y, alpha=0.5, edgecolor='black')
            plt.scatter(cell['site']['x'], cell['site']['y'], color='red')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Voronoi Diagram')
        plt.grid(True)
        plt.show()
    @staticmethod
    def generate_voronoi(points: List[Tuple[float, float]], bounds: Tuple[float, float, float, float]) -> List[Dict]:
        """生成泰森多边形"""
        points_array = np.array(points)
        delaunay = Delaunay(points_array)

        voronoi_cells = []
        for i, point in enumerate(points_array):
            cell = {
                'index': i + 1,
                'site': {'x': point[0], 'y': point[1]},
                'vertices': []
            }
            voronoi_cells.append(cell)

        # 计算泰森多边形顶点
        for i, simplex in enumerate(delaunay.simplices):
            tri = delaunay.points[simplex]
            circumcenter = VoronoiDiagram._calculate_circumcenter(tri[0], tri[1], tri[2])
            for j in range(3):
                neighbor = delaunay.neighbors[i][j]
                if neighbor != -1:
                    voronoi_cells[i]['vertices'].append(circumcenter)

        # 裁剪多边形
        for cell in voronoi_cells:
            cell['vertices'] = VoronoiDiagram._clip_polygon(cell['vertices'], bounds)

        return voronoi_cells

    @staticmethod
    def _calculate_circumcenter(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, float]:
        """计算三角形的外心"""
        ax = p2[0] - p1[0]
        ay = p2[1] - p1[1]
        bx = p3[0] - p1[0]
        by = p3[1] - p1[1]

        d = 2 * (ax * by - ay * bx)
        if d == 0:
            return (0, 0)

        cx = (by * (ax**2 + ay**2) - ay * (bx**2 + by**2)) / d
        cy = (ax * (bx**2 + by**2) - bx * (ax**2 + ay**2)) / d

        return (cx + p1[0], cy + p1[1])

    @staticmethod
    def _clip_polygon(vertices: List[Tuple[float, float]], bounds: Tuple[float, float, float, float]) -> List[Tuple[float, float]]:
        """使用Sutherland-Hodgman算法裁剪多边形"""
        left, right, bottom, top = bounds
        polygon = vertices.copy()

        def clip(polygon, edge):
            output_list = []
            s = polygon[-1]
            for point in polygon:
                if VoronoiDiagram._is_inside_edge(point, edge):
                    if not VoronoiDiagram._is_inside_edge(s, edge):
                        intersection = VoronoiDiagram._get_edge_intersection(s, point, edge)
                        output_list.append(intersection)
                    output_list.append(point)
                elif VoronoiDiagram._is_inside_edge(s, edge):
                    intersection = VoronoiDiagram._get_edge_intersection(s, point, edge)
                    output_list.append(intersection)
                s = point
            return output_list

        polygon = clip(polygon, 'left')
        polygon = clip(polygon, 'right')
        polygon = clip(polygon, 'bottom')
        polygon = clip(polygon, 'top')

        return polygon

    @staticmethod
    def _is_inside_edge(point: Tuple[float, float], edge: str) -> bool:
        x, y = point
        if edge == 'left':
            return x >= 0
        elif edge == 'right':
            return x <= 1000
        elif edge == 'bottom':
            return y >= 0
        elif edge == 'top':
            return y <= 1000
        return False

    @staticmethod
    def _get_edge_intersection(s: Tuple[float, float], p: Tuple[float, float], edge: str) -> Tuple[float, float]:
        x1, y1 = s
        x2, y2 = p
        if edge == 'left':
            return (0, y1 + (0 - x1) * (y2 - y1) / (x2 - x1))
        elif edge == 'right':
            return (1000, y1 + (1000 - x1) * (y2 - y1) / (x2 - x1))
        elif edge == 'bottom':
            return (x1 + (0 - y1) * (x2 - x1) / (y2 - y1), 0)
        elif edge == 'top':
            return (x1 + (1000 - y1) * (x2 - x1) / (y2 - y1), 1000)
        return (0, 0)
    
    
class InteriorOrientation:
    @staticmethod
    def calculate_interior_orientation(frame_marks, pixel_marks):
        """计算内定向参数"""
        A = []
        L = []
        for i in range(4):
            A.extend([
                [1, pixel_marks[i, 0], pixel_marks[i, 1], 0, 0, 0],
                [0, 0, 0, 1, pixel_marks[i, 0], pixel_marks[i, 1]]
            ])
            L.extend([frame_marks[i, 0], frame_marks[i, 1]])

        A = np.array(A)
        L = np.array(L)

        X = np.linalg.lstsq(A, L, rcond=None)[0]
        params = {
            'h0': X[0],
            'h1': X[1],
            'h2': X[2],
            'k0': X[3],
            'k1': X[4],
            'k2': X[5]
        }

        res = np.dot(A, X) - L
        resX = res[::2]
        resY = res[1::2]

        return params, resX, resY

    @staticmethod
    def pixel_to_image(pixels, params):
        """将像素坐标转换为图像坐标"""
        i = pixels[:, 0]
        j = pixels[:, 1]
        x = params['h0'] + params['h1'] * i + params['h2'] * j
        y = params['k0'] + params['k1'] * i + params['k2'] * j
        return np.column_stack((x, y))


class RelativeOrientation:
    @staticmethod
    def calculate_relative_orientation(left, right, f, B):
        """计算相对定向参数"""
        Bx = B[0]
        phi1, omega1, kappa1 = 0, 0, 0
        phi2, omega2, kappa2 = 0, 0, 0
        max_iter = 100
        tol = 1e-6

        for iter_count in range(max_iter):
            R1 = RelativeOrientation.get_rotation_matrix(phi1, omega1, kappa1)
            R2 = RelativeOrientation.get_rotation_matrix(phi2, omega2, kappa2)

            A = []
            L = []
            Q = np.zeros((len(left), 1))

            for k in range(len(left)):
                x1, y1 = left[k, 0], left[k, 1]
                left_space = np.dot(R1, np.array([x1, y1, -f]))
                X1, Y1, Z1 = left_space[0], left_space[1], left_space[2]

                x2, y2 = right[k, 0], right[k, 1]
                right_space = np.dot(R2, np.array([x2, y2, -f]))
                X2, Y2, Z2 = right_space[0], right_space[1], right_space[2]

                Ai = [-X1 * Y2 / Z1, X1, X2 * Y1 / Z1, -(Z1 - Y1 * Y2 / Z1), -X2]
                Li = f * Y1 / Z1 - f * Y2 / Z2

                A.append(Ai)
                L.append(Li)

            A = np.array(A)
            L = np.array(L)

            try:
                dX = np.linalg.lstsq(np.dot(A.T, A), np.dot(A.T, L), rcond=None)[0]
            except np.linalg.LinAlgError:
                break

            if np.max(np.abs(dX)) < tol:
                break

            phi1 += dX[0]
            kappa1 += dX[1]
            phi2 += dX[2]
            omega2 += dX[3]
            kappa2 += dX[4]

        params = {
            'phi1': phi1,
            'omega1': omega1,
            'kappa1': kappa1,
            'phi2': phi2,
            'omega2': omega2,
            'kappa2': kappa2
        }
        return params, Q, iter_count

    @staticmethod
    def get_rotation_matrix(phi, omega, kappa):
        """计算旋转矩阵"""
        a1 = np.cos(phi) * np.cos(kappa) - np.sin(phi) * np.sin(omega) * np.sin(kappa)
        a2 = -np.cos(phi) * np.sin(kappa) - np.sin(phi) * np.sin(omega) * np.cos(kappa)
        a3 = -np.sin(phi) * np.cos(omega)
        b1 = np.cos(omega) * np.sin(kappa)
        b2 = np.cos(omega) * np.cos(kappa)
        b3 = -np.sin(omega)
        c1 = np.sin(phi) * np.cos(kappa) + np.cos(phi) * np.sin(omega) * np.sin(kappa)
        c2 = -np.sin(phi) * np.sin(kappa) + np.cos(phi) * np.sin(omega) * np.cos(kappa)
        c3 = np.cos(phi) * np.cos(omega)

        return np.array([
            [a1, a2, a3],
            [b1, b2, b3],
            [c1, c2, c3]
        ])


class ForwardIntersection:
    @staticmethod
    def calculate_forward_intersection(left, right, rel_params, f, B):
        """计算前方交会"""
        R1 = RelativeOrientation.get_rotation_matrix(rel_params['phi1'], rel_params['omega1'], rel_params['kappa1'])
        R2 = RelativeOrientation.get_rotation_matrix(rel_params['phi2'], rel_params['omega2'], rel_params['kappa2'])

        n_points = len(left)
        X = np.zeros(n_points)
        Y = np.zeros(n_points)
        Z = np.zeros(n_points)
        deltaY = np.zeros(n_points)

        for k in range(n_points):
            S1 = np.array([0, 0, 0])
            S2 = np.array([B[0], 0, 0])

            vec1 = np.dot(R1, np.array([left[k, 0], left[k, 1], -f]))
            direction1 = vec1 / np.linalg.norm(vec1)

            vec2 = np.dot(R2, np.array([right[k, 0], right[k, 1], -f]))
            direction2 = vec2 / np.linalg.norm(vec2)

            A = np.column_stack((direction1, -direction2))
            b = S2 - S1

            try:
                lambda_val = np.linalg.lstsq(A, b, rcond=None)[0]
            except np.linalg.LinAlgError:
                lambda_val = np.array([0, 0])

            P = S1 + lambda_val[0] * direction1
            P2 = S2 + lambda_val[1] * direction2

            X[k] = P[0]
            Y[k] = P[1]
            Z[k] = P[2]
            deltaY[k] = P[1] - P2[1]

        return X, Y, Z, deltaY


class AbsoluteOrientation:
    @staticmethod
    def calculate_absolute_orientation(model_pts, ground_pts):
        """计算绝对定向参数"""
        model_mean = np.mean(model_pts, axis=0)
        ground_mean = np.mean(ground_pts, axis=0)

        model_centered = model_pts - model_mean
        ground_centered = ground_pts - ground_mean

        H = np.dot(model_centered.T, ground_centered)

        U, _, Vt = np.linalg.svd(H)
        R = np.dot(Vt.T, U.T)

        if np.linalg.det(R) < 0:
            Vt[2, :] *= -1
            R = np.dot(Vt.T, U.T)

        omega = np.arctan2(R[2, 1], R[2, 2])
        phi = -np.arcsin(R[2, 0])
        kappa = np.arctan2(R[1, 0], R[0, 0])

        sigma_model = np.sum(model_centered**2)
        sigma_ground = np.sum(ground_centered**2)
        scale = np.sqrt(sigma_ground / sigma_model)

        translation = ground_mean - scale * np.dot(model_mean, R.T)

        params = {
            'scale': scale,
            'tx': translation[0],
            'ty': translation[1],
            'tz': translation[2],
            'omega': omega,
            'phi': phi,
            'kappa': kappa,
            'R': R
        }

        transformed = scale * np.dot(model_pts, R.T) + translation
        residuals = ground_pts - transformed

        return params, residuals


class ResultOutput:
    @staticmethod
    def save_results(model_coords, ground_coords, file_path):
        """保存结果"""
        results = np.column_stack((ground_coords, model_coords))
        np.savetxt(file_path, results, delimiter=',', header='X,Y,Z,Xm,Ym,Zm', comments='')
class MagneticFieldCalculator:
    def __init__(self, mu0=4 * np.pi * 1e-7, I=1, c=1):
        """初始化常量"""
        self.mu0 = mu0  # 真空磁导率 (H/m)
        self.I = I       # 电流 (A)
        self.c = c       # 周长 (m)

    def calculate_B(self, N, x):
        """计算磁感应强度 B"""
        R = self.c / (2 * N * np.sin(np.pi / N))  # 半径 (m)
        B = np.zeros_like(x)
        cos_theta = np.cos(np.pi / N)
        sin_theta = np.sin(np.pi / N)

        denominator = (x**2 + R**2 * cos_theta**2) * np.sqrt(x**2 + R**2)
        B = self.mu0 * self.I * N * sin_theta**2 * cos_theta / (2 * np.pi * denominator)
        return B

    def plot_B_vs_x(self, N_values, x_range=(0, 0.5), num_points=100):
        """计算并绘制 B 随 x 的变化"""
        x = np.linspace(x_range[0], x_range[1], num_points)
        plt.figure()
        for N in N_values:
            B = self.calculate_B(N, x)
            plt.plot(x, B, label=f'N={N}')
        plt.xlabel('x (m)')
        plt.ylabel('B (T)')
        plt.title('磁感应强度 B 随轴线位置 x 的变化')
        plt.legend()
        plt.grid(True)
        plt.show()

    def calculate_B_max(self, N_values):
        """计算 B 的最大值对应的 N"""
        B_max = np.zeros(len(N_values))
        for idx, N in enumerate(N_values):
            R = self.c / (2 * N * np.sin(np.pi / N))
            cos_theta = np.cos(np.pi / N)
            sin_theta = np.sin(np.pi / N)
            denominator = (0**2 + R**2 * cos_theta**2) * np.sqrt(0**2 + R**2)
            B_max[idx] = self.mu0 * self.I * N * sin_theta**2 * cos_theta / (2 * np.pi * denominator)
        return B_max

    def plot_B_max_vs_N(self, N_values):
        """绘制 B_max 随 N 的变化"""
        B_max = self.calculate_B_max(N_values)
        plt.figure()
        plt.plot(N_values, B_max, '-o')
        plt.xlabel('N')
        plt.ylabel('B_max (T)')
        plt.title('B 的最大值随 N 的变化')
        plt.grid(True)
        plt.show()
class ContourGenerator:
    def __init__(self, dem_file_path: str, contour_interval: float = 10):
        """
        生成等高线的类
        :param dem_file_path: DEM文件路径
        :param contour_interval: 等高线间隔
        """
        self.dem_file_path = dem_file_path
        self.contour_interval = contour_interval
        self.dem_data = None
        self.x = None
        self.y = None

    def load_dem_data(self):
        """
        加载DEM数据
        """
        try:
            dem_dataset = gdal.Open(self.dem_file_path)
            band = dem_dataset.GetRasterBand(1)
            self.dem_data = band.ReadAsArray()
            self.x = np.arange(0, self.dem_data.shape[1], 1)
            self.y = np.arange(0, self.dem_data.shape[0], 1)
        except Exception as e:
            print(f"Error loading DEM data: {e}")

    def generate_contours(self):
        """
        生成等高线并显示
        """
        if self.dem_data is None:
            self.load_dem_data()

        levels = np.arange(np.min(self.dem_data), np.max(self.dem_data) + self.contour_interval, self.contour_interval)
        plt.figure()
        plt.contour(self.x, self.y, self.dem_data, levels=levels)
        plt.title('Contour Plot')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

class DelaunayTriangulator:
    def __init__(self, points: List[Tuple[float, float]]):
        """
        生成Delaunay三角网的类
        :param points: 点列表
        """
        self.points = points
        self.triangles = None

    def triangulate(self):
        """
        生成Delaunay三角网
        """
        try:
            self.triangles = Delaunay(self.points)
        except Exception as e:
            print(f"Error triangulating: {e}")

    def display_triangulation(self):
        """
        显示Delaunay三角网
        """
        if self.triangles is None:
            self.triangulate()

        plt.figure()
        plt.triplot(self.points[:, 0], self.points[:, 1], self.triangles.simplices)
        plt.title('Delaunay Triangulation')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

class DEMGenerator:
    def __init__(self, csv_file_path: str, x_col: str, y_col: str, z_col: str, resolution: int = 200):
        """
        生成DEM的类
        :param csv_file_path: CSV文件路径
        :param x_col: X列名
        :param y_col: Y列名
        :param z_col: Z列名
        :param resolution: DEM分辨率
        """
        self.csv_file_path = csv_file_path
        self.x_col = x_col
        self.y_col = y_col
        self.z_col = z_col
        self.resolution = resolution
        self.data = None
        self.dem_data = None
        self.x = None
        self.y = None

    def load_csv_data(self):
        """
        加载CSV数据
        """
        try:
            self.data = pd.read_csv(self.csv_file_path)
        except Exception as e:
            print(f"Error loading CSV data: {e}")

    def generate_dem(self):
        """
        生成DEM并显示
        """
        if self.data is None:
            self.load_csv_data()

        x = self.data[self.x_col].values
        y = self.data[self.y_col].values
        z = self.data[self.z_col].values

        xmin, xmax = np.min(x), np.max(x)
        ymin, ymax = np.min(y), np.max(y)
        xi = np.linspace(xmin, xmax, self.resolution)
        yi = np.linspace(ymin, ymax, self.resolution)
        self.x, self.y = np.meshgrid(xi, yi)

        self.dem_data = griddata((x, y), z, (self.x, self.y), method='linear')

        plt.figure()
        plt.contourf(self.x, self.y, self.dem_data)
        plt.colorbar(label='Elevation')
        plt.title('DEM')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

class SlopeCalculator:
    def __init__(self, dem_file_path: str):
        """
        计算坡度的类
        :param dem_file_path: DEM文件路径
        """
        self.dem_file_path = dem_file_path
        self.dem_data = None
        self.cellsize = None

    def load_dem_data(self):
        """
        加载DEM数据
        """
        try:
            with rasterio.open(self.dem_file_path) as src:
                self.dem_data = src.read(1)
                self.cellsize = src.res[0]
        except Exception as e:
            print(f"Error loading DEM data: {e}")

    def calculate_slope(self):
        """
        计算坡度并显示
        """
        if self.dem_data is None:
            self.load_dem_data()

        dzdx = np.gradient(self.dem_data, axis=1) / self.cellsize
        dzdy = np.gradient(self.dem_data, axis=0) / self.cellsize
        slope_radians = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
        slope_degrees = np.rad2deg(slope_radians)

        plt.figure()
        plt.imshow(slope_degrees, cmap='viridis')
        plt.colorbar(label='Slope (degrees)')
        plt.title('Slope')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()

class AspectCalculator:
    def __init__(self, dem_file_path: str):
        """
        计算坡向的类
        :param dem_file_path: DEM文件路径
        """
        self.dem_file_path = dem_file_path
        self.dem_data = None
        self.cellsize = None

    def load_dem_data(self):
        """
        加载DEM数据
        """
        try:
            with rasterio.open(self.dem_file_path) as src:
                self.dem_data = src.read(1)
                self.cellsize = src.res[0]
        except Exception as e:
            print(f"Error loading DEM data: {e}")

    def calculate_aspect(self):
        """
        计算坡向并显示
        """
        if self.dem_data is None:
            self.load_dem_data()

        dzdx = np.gradient(self.dem_data, axis=1) / self.cellsize
        dzdy = -np.gradient(self.dem_data, axis=0) / self.cellsize
        aspect = np.arctan2(dzdy, dzdx)
        aspect_degrees = (270 - np.degrees(aspect)) % 360

        plt.figure()
        plt.imshow(aspect_degrees, cmap='hsv')
        plt.colorbar(label='Aspect (degrees)')
        plt.title('Aspect')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
class HarrisCornerDetector:
    @staticmethod
    def corner_response(img, p):
        Ix = cv2.Sobel(img, cv2.CV_32F, 1, 0, 3)
        Iy = cv2.Sobel(img, cv2.CV_32F, 0, 1, 3)
        M = (Ix * Ix + Iy * Iy) - (Ix * Iy) ** 2
        return M[p]

    @staticmethod
    def build_dog_pyramid(img, levels):
        dog_pyramid = [img.copy()]
        current_level = img.copy()
        for _ in range(1, levels):
            current_level = cv2.pyrDown(current_level)
            dog_pyramid.append(current_level)
        return dog_pyramid

    @staticmethod
    def extract_corners(dog_pyramid):
        corners = []
        for i in range(len(dog_pyramid) - 1):
            scale = 1 << i
            k = 0.04 if i == len(dog_pyramid) - 2 else 0.06
            dog_level = dog_pyramid[i + 1] - dog_pyramid[i]
            G1 = cv2.Laplacian(dog_level, cv2.CV_32F)
            G1 = G1 ** 2
            G2 = dog_pyramid[i + 1] - 0.5 * (dog_pyramid[i] + dog_pyramid[i + 2])
            G2 = cv2.Laplacian(G2, cv2.CV_32F)
            G2 = G2 ** 2
            for j in range(dog_level.shape[0]):
                for k in range(dog_level.shape[1]):
                    if G1[j, k] > scale * k and G2[j, k] > scale * k:
                        corners.append((j, k))
        return corners

    def detect(self, img_path, harris_corners_num=200, harris_thresh=0.04, dog_levels=3):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray.astype(np.float32)
        gray = cv2.normalize(gray, None, 0, 1, cv2.NORM_MINMAX)

        harris_corners = []
        response_harris = 0
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                response = self.corner_response(gray, (i, j))
                if response > response_harris:
                    response_harris = response
                    harris_corners = [(j, i)]
                elif response > harris_thresh and response > gray[i, j]:
                    harris_corners.append((j, i))
        if len(harris_corners) > harris_corners_num:
            harris_corners = harris_corners[:harris_corners_num]

        dog_pyramid = self.build_dog_pyramid(gray, dog_levels)
        dog_corners = self.extract_corners(dog_pyramid)

        harris_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for corner in harris_corners:
            cv2.circle(harris_img, corner, 5, (0, 255, 0), -1)

        dog_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for corner in dog_corners:
            cv2.circle(dog_img, corner, 5, (0, 0, 255), -1)

        return harris_img, dog_img
class ImageTransformer:
    @staticmethod
    def py_transform(src_image):
        src_rows, src_cols = src_image.shape
        src_points = [np.float32([0, 0]), np.float32([src_cols - 1, 0]), np.float32([0, src_rows - 1])]
        res_points = [np.float32([114, 114]), np.float32([src_cols + 114, 114]), np.float32([114, src_rows + 114])]
        return cv2.getAffineTransform(src_points, res_points)

    @staticmethod
    def xz_transform(src_image):
        src_rows, src_cols = src_image.shape
        src_points = [np.float32([0, 0]), np.float32([src_cols - 1, 0]), np.float32([0, src_rows - 1])]
        res_points = [np.float32([src_cols * 0.7, src_rows * 0]), np.float32([src_cols * 1, src_rows * 0.7]), np.float32([src_cols * 0, src_rows * 0.7])]
        return cv2.getAffineTransform(src_points, res_points)

    @staticmethod
    def sf_transform(src_image):
        src_rows, src_cols = src_image.shape
        src_points = [np.float32([0, 0]), np.float32([src_cols - 1, 0]), np.float32([0, src_rows - 1])]
        res_points = [np.float32([50, 50]), np.float32([src_cols - 50, 50]), np.float32([50, src_rows - 50])]
        return cv2.getAffineTransform(src_points, res_points)

    @staticmethod
    def fs_transform(src_image):
        src_rows, src_cols = src_image.shape
        src_points = [np.float32([0, 0]), np.float32([src_cols - 1, 0]), np.float32([0, src_rows - 1])]
        res_points = [np.float32([0, src_rows * 0.33]), np.float32([src_cols * 0.8, src_rows * 0.2]), np.float32([src_cols * 0.2, src_rows * 0.3])]
        return cv2.getAffineTransform(src_points, res_points)

    def transform(self, img_path):
        img = cv2.imread(img_path, 0)
        warp_mat = self.py_transform(img)
        warp_mat_ = cv2.invertAffineTransform(warp_mat)
        result_img = np.zeros_like(img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                uv = np.array([[i], [j], [1]], dtype=np.float32)
                xy = np.dot(warp_mat_, uv)
                x, y = int(xy[0, 0]), int(xy[1, 0])
                if 0 <= x < img.shape[0] and 0 <= y < img.shape[1]:
                    result_img[j, i] = img[y, x]
        cv2.imwrite(img_path.replace('.png', '_pingyi.png'), result_img)

        res2 = np.zeros_like(img)
        warp_mat = self.xz_transform(img)
        cv2.warpAffine(img, warp_mat, res2.shape, res2)
        cv2.imwrite(img_path.replace('.png', '_roll.png'), res2)

        res3 = np.zeros_like(img)
        warp_mat = self.fs_transform(img)
        cv2.warpAffine(img, warp_mat, res3.shape, res3)
        cv2.imwrite(img_path.replace('.png', '_fangshe.png'), res3)

        xkd = 9999  # Reduced size
        xgd = 9999  # Reduced size
        jlcz = cv2.resize(img, (xkd, xgd), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(img_path.replace('.png', '_jlcz.png'), jlcz)

        xxgd = cv2.resize(img, (xkd, xgd), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(img_path.replace('.png', '_xxgd.png'), xxgd)
class ImageFilter:
    @staticmethod
    def jq_filter(tp, qz):
        hedaxiao = len(qz)
        yiban = hedaxiao // 2
        mb = np.zeros((tp.shape[0] - 2 * yiban, tp.shape[1] - 2 * yiban), dtype=tp.dtype)
        for i in range(yiban, tp.shape[0] - yiban):
            for j in range(yiban, tp.shape[1] - yiban):
                sum_val = 0.0
                for k in range(-yiban, yiban + 1):
                    for l in range(-yiban, yiban + 1):
                        sum_val += qz[k * hedaxiao + l] * tp[i - k, j - l][0]
                mb[i - yiban, j - yiban] = sum_val
        return mb

    @staticmethod
    def zz_filter(tp, dx):
        yiban = dx // 2
        mb = np.zeros((tp.shape[0] - 2 * yiban, tp.shape[1] - 2 * yiban), dtype=tp.dtype)
        for i in range(yiban, tp.shape[0] - yiban):
            for j in range(yiban, tp.shape[1] - yiban):
                pixel_values = []
                for k in range(-yiban, yiban + 1):
                    for l in range(-yiban, yiban + 1):
                        pixel_values.append(tp[i + k, j + l][0])
                pixel_values.sort()
                mb[i - yiban, j - yiban] = pixel_values[(dx * dx) // 2]
        return mb

    @staticmethod
    def jyz_filter(tp, xd):
        mb = tp.copy()
        for i in range(tp.shape[0]):
            for j in range(tp.shape[1]):
                if np.random.rand() < xd:
                    mb[i, j][0] = 255 if np.random.rand() > 0.5 else 0
        return mb

    @staticmethod
    def cf_filter(tp):
        sobel_x = cv2.Sobel(tp, cv2.CV_32F, 1, 0)
        sobel_y = cv2.Sobel(tp, cv2.CV_32F, 0, 1)
        mb = np.zeros_like(tp)
        cv2.cartToPolar(sobel_x, sobel_y, mb, sobel_x)
        return mb

    def apply_filter(self, img_path, filter_type, params):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if filter_type == 'jq':
            quanzhong = [1, 2, 1, 2, 1, 2, 1, 2, 1]
            result = self.jq_filter(gray, quanzhong)
            cv2.imwrite(img_path.replace('.png', '_jiaquan.png'), result)
        elif filter_type == 'zz':
            result = self.zz_filter(gray, params)
            cv2.imwrite(img_path.replace('.png', '_zhongzhi.png'), result)
        elif filter_type == 'jyz':
            result = self.jyz_filter(gray, params)
            cv2.imwrite(img_path.replace('.png', '_jiaoyan.png'), result)
        elif filter_type == 'cf':
            result = self.cf_filter(gray)
            cv2.imwrite(img_path.replace('.png', '_chafen.png'), result)
class LOGDetector:
    @staticmethod
    def gslpls(cd, ztfbcs):
        hx = np.zeros((cd, cd), dtype=np.double)
        ybcd = cd // 2
        for i in range(-ybcd, ybcd + 1):
            for j in range(-ybcd, ybcd + 1):
                hx[i + ybcd, j + ybcd] = np.exp(-((j ** 2 + i ** 2) / (2 * ztfbcs ** 2))) * ((j ** 2 + i ** 2 - 2 * ztfbcs ** 2) / (2 * ztfbcs ** 4))
        return hx

    @staticmethod
    def byjc(img, cd):
        ker_offset = cd // 2
        hx = LOGDetector.gslpls(cd, 1.6)
        laplacian = np.zeros((img.shape[0] - 2 * ker_offset, img.shape[1] - 2 * ker_offset), dtype=np.double)
        jg = np.zeros((laplacian.shape[0], laplacian.shape[1]), dtype=img.dtype)
        for i in range(ker_offset, img.shape[0] - ker_offset):
            for j in range(ker_offset, img.shape[1] - ker_offset):
                sum_laplacian = 0
                for k in range(-ker_offset, ker_offset + 1):
                    for m in range(-ker_offset, ker_offset + 1):
                        sum_laplacian += img[i + k, j + m] * hx[ker_offset + k, ker_offset + m]
                laplacian[i - ker_offset, j - ker_offset] = sum_laplacian
        for x in range(1, jg.shape[0] - 1):
            for y in range(1, jg.shape[1] - 1):
                jg[x, y] = 0
                if laplacian[x - 1, y] * laplacian[x + 1, y] < 0:
                    jg[x, y] = 255
                if laplacian[x, y - 1] * laplacian[x, y + 1] < 0:
                    jg[x, y] = 255
        return jg

    def detect(self, img_path, cd=9):
        img = cv2.imread(img_path, 0)
        edge = self.byjc(img, cd)
        return edge
class HistogramCalculator:
    @staticmethod
    def calculate_histogram(img_path):
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        histogram = np.zeros(256, dtype=np.int32)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                index = image[i, j]
                histogram[index] += 1
        return histogram

    @staticmethod
    def draw_histogram(histogram):
        draw_image = np.zeros((400, 500, 3), dtype=np.uint8)
        for i in range(256):
            value = cv2.Round(histogram[i] * 256 * 0.5)
            cv2.rectangle(draw_image, (i, draw_image.shape[0] - 1), (i, draw_image.shape[0] - 1 - value), (255, 255, 255), -1)
        return draw_image

    def calculate_and_draw(self, img_path):
        histogram = self.calculate_histogram(img_path)
        draw_image = self.draw_histogram(histogram)
        return draw_image
class PerformanceComparator:
    @staticmethod
    def scgsjz(n, ztfbcs):
        jjh = np.zeros((n, n), dtype=np.double)
        m = n // 2
        for i in range(-m, m + 1):
            for j in range(-m, m + 1):
                jjh[i + m, j + m] = np.exp(-((j ** 2 + i ** 2) / (2 * ztfbcs ** 2))) * (1 / (2 * 3.14 * ztfbcs ** 2))
        return jjh

    @staticmethod
    def log_transform(img, n):
        n_rows, n_cols = img.shape
        m = n // 2
        gsjz = PerformanceComparator.scgsjz(n, 1.6)
        gsmh = np.zeros((n_rows - 2 * m, n_cols - 2 * m), dtype=np.double)
        for i in range(m, n_rows - m):
            for j in range(m, n_cols - m):
                temp = img[i - m:i + m + 1, j - m:j + m + 1]
                gsmh[i - m, j - m] = np.sum(temp * gsjz)
        lap = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.double)
        tx = np.zeros((n_rows - 2 * m - 2, n_cols - 2 * m - 2), dtype=np.double)
        for i in range(m + 1, n_rows - m - 1):
            for j in range(m + 1, n_cols - m - 1):
                temp = gsmh[i - m - 1:i - m + 2, j - m - 1:j - m + 2]
                tx[i - m - 1, j - m - 1] = np.sum(temp * lap)
        return tx

    @staticmethod
    def dog_transform(img, n):
        n_rows, n_cols = img.shape
        m = n // 2
        gsjz = PerformanceComparator.scgsjz(n, 0.7)
        gsjz2 = PerformanceComparator.scgsjz(n, 0.8)
        gsjz = gsjz - gsjz2
        goutu = np.zeros((n_rows - 2 * m, n_cols - 2 * m), dtype=np.double)
        for i in range(m, n_rows - m):
            for j in range(m, n_cols - m):
                temp = img[i - m:i + m + 1, j - m:j + m + 1]
                goutu[i - m, j - m] = np.sum(temp * gsjz)
        return goutu

    def compare(self, img_path, n=9):
        img = cv2.imread(img_path, 0)
        start_time = time.time()
        goutu = self.dog_transform(img, n)
        dog_time = time.time() - start_time
        print(f"DOG Time: {dog_time}")
        cv2.imshow("DOG Result", goutu)
        cv2.waitKey(0)

        start_time = time.time()
        logtu = self.log_transform(img, n)
        log_time = time.time() - start_time
        print(f"LOG Time: {log_time}")
        cv2.imshow("LOG Result", logtu)
        cv2.waitKey(0)



class GaussForward:
    def __init__(self, B1, L1, s12, A12):
        self.B1 = B1
        self.L1 = L1
        self.s12 = s12
        self.A12 = A12
        self.a = 6378137  # 地球半径
        self.f = 1 / 298.257223563  # 扁率
        self.e = math.sqrt(self.f)  # 第一偏心率
        self.e2 = self.e**2  # 第一偏心率平方
        self.e2p = self.e2 / (1 - self.e2)  # 第一偏心率平方加一

    def dms_to_decimal(self, degrees, minutes, seconds):
        return degrees + minutes / 60 + seconds / 3600

    def decimal_to_dms(self, decimal):
        degrees = int(decimal)
        minutes = int((decimal - degrees) * 60)
        seconds = (decimal - degrees - minutes / 60) * 3600
        return degrees, minutes, seconds

    def calculate_gauss_parameters(self):
        B1_rad = math.radians(self.B1)
        L1_rad = math.radians(self.L1)
        N = self.a / math.sqrt(1 - self.e2 * math.sin(B1_rad)**2)
        t = math.tan(B1_rad)
        eta = self.e2p * math.sin(B1_rad)
        A = math.cos(B1_rad)
        M = N * math.cos(B1_rad)
        m = M / (2 * self.a) * (1 - self.e2 / 4 - 3 * self.e2**2 / 64 - 5 * self.e2**3 / 256)
        U = M + m * (L1_rad**2 + 3 * L1_rad**4 * (1 - t**2) + 5 * L1_rad**6 * (1 - 3 * t**2 + 3 * t**4))
        V = N * (1 - self.e2 * (1 - t**2) / 4 - 3 * self.e2**2 * (1 - t**2)**2 / 64 - 5 * self.e2**3 * (1 - t**2)**3 / 256)
        return N, t, eta, A, M, m, U, V

    def forward_gauss(self):
        N, t, eta, A, M, m, U, V = self.calculate_gauss_parameters()
        A12_rad = math.radians(self.A12)
        x = self.s12 * math.cos(A12_rad) + U
        y = self.s12 * math.sin(A12_rad) + V
        return x, y


# 高斯引数反算类
class GaussInverse:
    def __init__(self, B1, L1, x, y):
        self.B1 = B1
        self.L1 = L1
        self.x = x
        self.y = y
        self.a = 6378137  # 地球半径
        self.f = 1 / 298.257223563  # 扁率
        self.e = math.sqrt(self.f)  # 第一偏心率
        self.e2 = self.e**2  # 第一偏心率平方
        self.e2p = self.e2 / (1 - self.e2)  # 第一偏心率平方加一

    def calculate_gauss_parameters(self):
        B1_rad = math.radians(self.B1)
        L1_rad = math.radians(self.L1)
        N = self.a / math.sqrt(1 - self.e2 * math.sin(B1_rad)**2)
        t = math.tan(B1_rad)
        eta = self.e2p * math.sin(B1_rad)
        A = math.cos(B1_rad)
        M = N * math.cos(B1_rad)
        m = M / (2 * self.a) * (1 - self.e2 / 4 - 3 * self.e2**2 / 64 - 5 * self.e2**3 / 256)
        U = M + m * (L1_rad**2 + 3 * L1_rad**4 * (1 - t**2) + 5 * L1_rad**6 * (1 - 3 * t**2 + 3 * t**4))
        V = N * (1 - self.e2 * (1 - t**2) / 4 - 3 * self.e2**2 * (1 - t**2)**2 / 64 - 5 * self.e2**3 * (1 - t**2)**3 / 256)
        return N, t, eta, A, M, m, U, V

    def inverse_gauss(self):
        N, t, eta, A, M, m, U, V = self.calculate_gauss_parameters()
        s12 = math.sqrt((self.x - U)**2 + (self.y - V)**2)
        A12_rad = math.atan2(self.y - V, self.x - U)
        A12 = math.degrees(A12_rad)
        L1 = math.atan((self.y - V) / (self.x - U))
        B1 = math.atan((1 - self.e2 * N / (N + s12)) * math.tan(math.radians(self.B1)))
        return math.degrees(B1), math.degrees(L1), s12, A12
# 测边交会类
class SideIntersection:
    def __init__(self, x1, y1, x2, y2, sa, sb):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.sa = sa
        self.sb = sb

    def calculate(self):
        c = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)
        a = math.acos((-self.sa**2 + self.sb**2 + c**2) / (2 * self.sb * c))
        b = math.acos((self.sa**2 - self.sb**2 + c**2) / (2 * self.sa * c))
        xp = (self.x1 * math.tan(a) + self.x2 * math.tan(b) + (self.y2 - self.y1) * math.tan(a) * math.tan(b)) / (math.tan(a) + math.tan(b))
        yp = (self.y1 * math.tan(a) + self.y2 * math.tan(b) + (self.x2 - self.x1) * math.tan(a) * math.tan(b)) / (math.tan(a) + math.tan(b))
        return xp, yp


# 测角交会类
class AngleIntersection:
    def __init__(self, x1, y1, x2, y2, a, b):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = math.radians(a)
        self.b = math.radians(b)

    def calculate(self):
        xp = (self.x1 * math.tan(self.a) + self.x2 * math.tan(self.b) + (self.y2 - self.y1) * math.tan(self.a) * math.tan(self.b)) / (math.tan(self.a) + math.tan(self.b))
        yp = (self.y1 * math.tan(self.a) + self.y2 * math.tan(self.b) + (self.x2 - self.x1) * math.tan(self.a) * math.tan(self.b)) / (math.tan(self.a) + math.tan(self.b))
        return xp, yp


# 边角交会类
class SideAngleIntersection:
    def __init__(self, x1, y1, x2, y2, jcg):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.jcg = jcg

    def calculate(self):
        c = math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)
        a = math.radians(44.7766)
        b = math.radians(86.0681)
        jc = math.pi - a - b
        jcd = math.degrees(jc)
        fb = jcd - self.jcg
        if abs(fb) < 60 * math.sqrt(3):
            a = math.radians(a - 1/3 * fb)
            b = math.radians(b - 1/3 * fb)
            xp = (self.x1 * math.tan(a) + self.x2 * math.tan(b) + (self.y2 - self.y1) * math.tan(a) * math.tan(b)) / (math.tan(a) + math.tan(b))
            yp = (self.y1 * math.tan(a) + self.y2 * math.tan(b) + (self.x2 - self.x1) * math.tan(a) * math.tan(b)) / (math.tan(a) + math.tan(b))
            return xp, yp
        else:
            return None, None


# 后方交会类
class BackwardIntersectionceliangxue:
    def __init__(self, ra, rb, xa, xb, xc, ya, yb, yc):
        self.ra = math.radians(ra)
        self.rb = math.radians(rb)
        self.xa = xa
        self.xb = xb
        self.xc = xc
        self.ya = ya
        self.yb = yb
        self.yc = yc

    def calculate_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def calculate_angle(self, x1, y1, x2, y2, x3, y3):
        a = self.calculate_distance(x1, y1, x2, y2)
        b = self.calculate_distance(x2, y2, x3, y3)
        c = self.calculate_distance(x1, y1, x3, y3)
        angle1 = math.acos((a**2 + b**2 - c**2) / (2 * a * b))
        angle2 = math.acos((b**2 + c**2 - a**2) / (2 * b * c))
        angle3 = math.acos((c**2 + a**2 - b**2) / (2 * c * a))
        return angle1, angle2, angle3

    def calculate(self):
        rc = 360 - math.degrees(self.ra) - math.degrees(self.rb)
        a = math.radians(rc - math.degrees(self.rb))
        b = math.radians(math.degrees(self.ra) - rc)
        c = math.radians(math.degrees(self.rb) - math.degrees(self.ra))
        angleA, angleB, angleC = self.calculate_angle(self.xa, self.ya, self.xb, self.yb, self.xc, self.yc)
        pa = (math.tan(a) * math.tan(angleA)) / (math.tan(a) - math.tan(angleA))
        pb = (math.tan(b) * math.tan(angleB)) / (math.tan(b) - math.tan(angleB))
        pc = (math.tan(c) * math.tan(angleC)) / (math.tan(c) - math.tan(angleC))
        xp = (pa * self.xa + pb * self.xb + pc * self.xc) / (pa + pb + pc)
        yp = (pa * self.ya + pb * self.yb + pc * self.yc) / (pa + pb + pc)
        return xp, yp
    
class EightParameterTransformation:
    def __init__(self, file_path):
        self.file_path = file_path
        self.matrix = None
        self.Lefg0 = None
        self.load_matrix()

    def load_matrix(self):
        try:
            df = pd.read_excel(self.file_path, header=None, skiprows=0)
            self.matrix = df.values
        except Exception as e:
            print(f"读取Excel文件时出错: {e}")

    def find_parameter(self):
        if self.matrix is None or self.matrix.size == 0:
            print("未成功获取矩阵，请检查文件内容。")
            return None

        num_rows = self.matrix.shape[0]
        A = np.zeros((2 * num_rows, 8))
        for i in range(num_rows):
            a = 2 * i
            b = 2 * i + 1
            A[a][0] = self.matrix[i][0]
            A[a][2] = -self.matrix[i][0] * self.matrix[i][2]
            A[a][3] = self.matrix[i][1]
            A[a][5] = -self.matrix[i][1] * self.matrix[i][2]
            A[a][6] = 1
            A[b][1] = self.matrix[i][0]
            A[b][2] = -self.matrix[i][0] * self.matrix[i][3]
            A[b][4] = self.matrix[i][1]
            A[b][5] = -self.matrix[i][1] * self.matrix[i][3]
            A[b][7] = 1

        B = np.zeros((2 * num_rows, 1))
        for i in range(num_rows):
            a = 2 * i
            b = 2 * i + 1
            B[a][0] = self.matrix[i][2]
            B[b][0] = self.matrix[i][3]

        W = B
        P = Q = np.eye(8)
        N = np.dot(A, np.dot(Q, A.T))
        K = np.dot(np.linalg.pinv(N), W)
        V = np.dot(Q, np.dot(A.T, K))

        self.Lefg0 = V.flatten()
        print("8参数平差值:", self.Lefg0)

        delta = math.sqrt(np.dot(V.T, np.dot(P, V)) / (2 * num_rows))
        print("单位权方差:", delta)
        return self.Lefg0

    def check(self):
        if self.Lefg0 is None or self.matrix is None:
            print("请先计算8参数。")
            return

        num_rows = self.matrix.shape[0]
        A = np.zeros((num_rows, 2))
        for i in range(num_rows):
            denominator = self.Lefg0[2] * self.matrix[i][0] + self.Lefg0[5] * self.matrix[i][1] + 1
            A[i][0] = (self.Lefg0[0] * self.matrix[i][0] + self.Lefg0[3] * self.matrix[i][1] + self.Lefg0[6]) / denominator
            A[i][1] = (self.Lefg0[1] * self.matrix[i][0] + self.Lefg0[4] * self.matrix[i][1] + self.Lefg0[7]) / denominator

        B = np.zeros((num_rows, 2))
        for i in range(num_rows):
            B[i][0] = self.matrix[i][2] - A[i][0]
            B[i][1] = self.matrix[i][3] - A[i][1]

        print("残差:", B)

        RMSE = math.sqrt(np.sum(np.square(B)) / (2 * num_rows))
        print("中误差:", RMSE)

    def find_Coordinate(self):
        if self.Lefg0 is None or self.matrix is None:
            print("请先计算8参数。")
            return

        num_rows = self.matrix.shape[0]
        A = np.zeros((num_rows, 2))
        for i in range(num_rows):
            denominator = self.Lefg0[2] * self.matrix[i][0] + self.Lefg0[5] * self.matrix[i][1] + 1
            A[i][0] = (self.Lefg0[0] * self.matrix[i][0] + self.Lefg0[3] * self.matrix[i][1] + self.Lefg0[6]) / denominator
            A[i][1] = (self.Lefg0[1] * self.matrix[i][0] + self.Lefg0[4] * self.matrix[i][1] + self.Lefg0[7]) / denominator

        print("变换后的坐标:", A)

    def transform_coordinates(self, check_points):
        if self.Lefg0 is None:
            print("请先计算8参数。")
            return

        num_rows = check_points.shape[0]
        transformed_coords = np.zeros((num_rows, 2))
        for i in range(num_rows):
            denominator = self.Lefg0[2] * check_points[i][0] + self.Lefg0[5] * check_points[i][1] + 1
            transformed_coords[i][0] = (self.Lefg0[0] * check_points[i][0] + self.Lefg0[3] * check_points[i][1] + self.Lefg0[6]) / denominator
            transformed_coords[i][1] = (self.Lefg0[1] * check_points[i][0] + self.Lefg0[4] * check_points[i][1] + self.Lefg0[7]) / denominator

        return transformed_coords

    def plot_transformed_points(self, transformed_coords):
        if transformed_coords is None:
            print("无坐标点可绘制。")
            return

        plt.figure(figsize=(10, 6))
        for i in range(len(transformed_coords) - 1):
            plt.plot([transformed_coords[i][0], transformed_coords[i+1][0]],
                     [transformed_coords[i][1], transformed_coords[i+1][1]], 'bo-')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Transformed Key Points')
        plt.grid(True)
        plt.show()


