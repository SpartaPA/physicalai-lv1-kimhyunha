from setuptools import find_packages, setup
package_name = 'turtle_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pa',
    maintainer_email='visualkhh@gmail.com',
    description='turtle_py',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_square = turtle_py.square_node:main',
            'turtle_alarm = turtle_py.alarm_node:main',
            'turtle_distance = turtle_py.distance_node:main',
            'turtle_rotate = turtle_py.rotate_client:main',
        ],
    },
)
