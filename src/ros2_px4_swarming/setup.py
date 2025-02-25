import os
from setuptools import setup
from glob import glob

package_name = 'ros2_px4_swarming'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'parameters'), glob('parameters/*.yaml'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dellwork1',
    maintainer_email='dellwork1@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'targetRover = ros2_px4_swarming.targetRover:main',
            'anchorDrone = ros2_px4_swarming.anchorDrone:main',
            'trackingVelocityCalculator = ros2_px4_swarming.trackingVelocityCalculator:main',
            'performanceAnalyzer = ros2_px4_swarming.performanceAnalyzer:main',
            'numAnchorsNode = ros2_px4_swarming.numAnchorsNode:main',
            'GPSSimulator = ros2_px4_swarming.GPSSimulator:main',
            'printInformationNode = ros2_px4_swarming.printInformationNode:main',
            'topicsRecorder = ros2_px4_swarming.topicsRecorder:main'
        ],
    },
)
