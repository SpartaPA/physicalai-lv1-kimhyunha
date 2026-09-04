from setuptools import find_packages, setup
package_name = 'turtle_custom_interface_py'
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pa',
    maintainer_email='visualkhh@gmail.com',
    description='DrawPolygon action server + WaypointList publisher',
    license='MIT',
    entry_points={
        'console_scripts': [
            'draw_polygon_server = turtle_custom_interface_py.draw_polygon_server:main',
            'waypoint_publisher = turtle_custom_interface_py.waypoint_publisher:main',
        ],
    },
)
