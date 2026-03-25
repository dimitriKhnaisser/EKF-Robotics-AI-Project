from setuptools import find_packages, setup

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        ('share/' + package_name + '/launch', [
            'launch/spawn_minimal_robot.launch.py',
            'launch/spawn_my_robot.launch.py',
            'launch/ekf.launch.py'
        ]),
        ('share/' + package_name + '/config', ['config/ekf.yaml']),
        ('share/' + package_name + '/urdf', ['urdf/my_robot.urdf']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dimi',
    maintainer_email='dimi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'auto_rectangle = my_robot_pkg.auto_rectangle:main',
            'ground_truth_extraction = my_robot_pkg.ground_truth_extraction:main',
            'noisy_odom = my_robot_pkg.noisy_odom:main',
            'noisy_data_extraction = my_robot_pkg.noisy_data_extraction:main',
            'imu_fix = my_robot_pkg.imu_fix:main',
            'ekf_data_extraction = my_robot_pkg.ekf_data_extraction:main'


        ],
    },
)
