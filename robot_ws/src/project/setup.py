from setuptools import setup

package_name = 'a_team'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cshe97',
    maintainer_email='cshe97@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'Line_trace = Line_trace:main',
        'Auto_driving = Auto_driving:main',
        'pub_pt_msg = a_team.pub_pt_msg:main',
        'servo_control = servo_control:main',
        ],
    },
)
