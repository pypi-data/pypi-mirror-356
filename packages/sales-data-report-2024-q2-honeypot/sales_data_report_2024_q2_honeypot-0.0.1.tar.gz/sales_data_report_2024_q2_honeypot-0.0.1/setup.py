import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sales-data-report-2024-q2-honeypot", 
    version="0.0.1", # 버전 (처음엔 0.0.1부터 시작)
    author="duckoo", # 본인 이름
    author_email="nonoyas@naver.com", # 본인 이메일
    description="This is a demo sales report package for Q2 2024. For more details, please refer to: http://nonoyas.pythonanywhere.com/honey.gif?token=sales_report_2024_Q2",

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-github-username/sales-report-demo-2024-q2", # 패키지 관련 URL (옵션)
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)