from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orange3-autogluon-timeseries",
    version="1.4.7",  # ← УВЕЛИЧИЛИ версию для новой функциональности
    description="AutoGluon Time Series forecasting widget for Orange3 with local Chronos support",  # ← ОБНОВИЛИ описание
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Иван Кордяк",
    author_email="KordyakIM@gmail.com",
    url="https://github.com/KordyakIM/autogluon-timeseries-widget",
    license="MIT",
    packages=find_namespace_packages(include=["orangecontrib*"]),
    namespace_packages=["orangecontrib"],
    package_data={
        "orangecontrib.autogluon_timeseries.widgets": ["icons/*.png"],
    },
    entry_points={
        "orange.widgets": (
            "AutoGluon Time Series = orangecontrib.autogluon_timeseries.widgets",
        ),
        "orange.canvas.help": (
            "html-index = orangecontrib.autogluon_timeseries.widgets:WIDGET_HELP_PATH",
        )
    },
    install_requires=[
        "Orange3>=3.38.1",
        "autogluon.timeseries>=1.3.1",
        "pandas>=2.2,<2.3",
        "numpy>=1.25",
        "PyQt5>=5.15",
        "matplotlib>=3.5",
        "holidays>=0.20",
        
        # ========== НОВЫЕ ЗАВИСИМОСТИ ==========
        "requests>=2.25.0",        # Для проверки интернет-соединения
        "transformers>=4.30.0",    # Для работы с Chronos моделями
        "huggingface-hub>=0.16.0", # Для кеширования и загрузки моделей
        "torch>=2.0.0",           # PyTorch для Chronos (если еще не установлен)
        "safetensors>=0.3.0",     # Для загрузки весов моделей
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",  # ← ДОБАВИЛИ поддержку 3.10
        "Programming Language :: Python :: 3.11",  # ← ДОБАВИЛИ поддержку 3.11
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",  # ← ДОБАВИЛИ
    ],
    keywords=[
        "orange3 add-on", "time series", "forecasting", "autogluon", 
        "chronos", "local models", "offline"  # ← ДОБАВИЛИ новые ключевые слова
    ],
    python_requires=">=3.9",
)