from setuptools import setup, find_packages

setup(
    name="potato-chat-ip-bot",
    version="1.0.0",
    description="Chinese IP geolocation bot for Potato Chat",
    packages=find_packages(),
    install_requires=[
        "pytelegrambotapi>=4.28.0",
        "requests>=2.32.4",
    ],
    python_requires=">=3.11",
)