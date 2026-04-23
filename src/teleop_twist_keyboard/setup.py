from setuptools import setup

package_name = 'teleop_twist_keyboard'

setup(
    name=package_name,
    version='2.4.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jbohren',
    maintainer_email='jbo@jhu.edu',
    description='Teleop_twist_keyboard with modified key bindings',
    license='BSD',
    entry_points={
        'console_scripts': [
            'teleop_twist_keyboard = teleop_twist_keyboard.teleop_twist_keyboard:main',
        ],
    },
)
