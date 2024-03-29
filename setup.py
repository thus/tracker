try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='tracker',
    version='1.0.0',
    description="Device tracking for home automation",
    author="Mats Klepsland",
    author_email='mats.klepsland@gmail.com',
    packages=[
        'tracker', 'tracker.modules'
    ],
    package_dir={'tracker':
                 'tracker'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tracker=tracker.tracker:main'
        ],
    },
    install_requires=[],
    zip_safe=False,
    keywords='tracker',
    test_suite='tests',
)
