from setuptools import setup, find_packages

setup(name='ninfo-plugin-infoblox',
    version='0.4',
    zip_safe=False,
    packages = find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "ninfo>=0.1.11",
        "infoblox",
    ],
    entry_points = {
        'ninfo.plugin': [
            'infoblox     = ninfo_plugin_infoblox',
        ]
    }
) 
