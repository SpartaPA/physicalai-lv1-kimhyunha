from setuptools import find_packages, setup
package_name = 'turtle_visualize_record_test_py'
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
    description='TF + Marker + pytest',
    license='MIT',
    entry_points={
        'console_scripts': [
            'tf_broadcaster = turtle_visualize_record_test_py.tf_broadcaster:main',
            'marker_publisher = turtle_visualize_record_test_py.marker_publisher:main',
        ],
    },
)
