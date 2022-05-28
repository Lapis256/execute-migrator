from setuptools import setup

setup(
    name="execute-migrator",
    version="1.0.0",
    install_requires=[
        "amulet-nbt>=1.2.0,<1.3.0",
        "mcfunction-be.py@git+https://github.com/Lapis256/mcfunction-be.py.git",
    ],
    extras_require={
        ":sys_platform == 'linux' and platform_machine == 'aarch64'": [
            "bedrock@git+https://github.com/Lapis256/bedrock@master"
        ],
        ":platform_machine != 'aarch64'": [
            "bedrock@git+https://github.com/BluCodeGH/bedrock@master"
        ],
    },
    packages=["execute_migrator"],
    entry_points={
        "console_scripts": ["execute_migrator = execute_migrator.__main__:main"]
    },
)
