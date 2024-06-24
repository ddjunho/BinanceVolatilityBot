from setuptools import setup

setup(
    name="BinanceVolatilityBot",
    version="0.1.0",
    install_requires=[
        'pandas',
        'ccxt',
        'schedule',
        'pmdarima',
        'telepot',
    ],
)
