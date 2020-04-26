import setuptools

setuptools.setup(name='hltv-scraping',
                 version='1',
                 description='Scraping data from hltv.org',
                 url='https://github.com/crazyhitty/hltv-scraping',
                 author='Kartik Sharma',
                 author_email='kartik.sharma.og@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 install_requires=['scrapy'])
