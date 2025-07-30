from setuptools import setup


setup(
  name = 'invoicing-pdf_20-06-2025',         #* Your package will have this name
  packages = ['invoicing'],   #* Name the package again
  version = '1.0.0',         #* To be increased every time your change your library
  license='MIT',             # Type of license. More here: https://help.github.com/articles/licensing-a-repository
  description = 'This package can ALSO be used to convert Excel invoices to PDF invoices.',    # Short description of your library
  author = 'cookiemonster',                   # Your name
  author_email = 's02934875@gmail.com',  # Your email
  url = 'https://example.com',              # Homepage of your library (e.g. github or your website)
  keywords = ['invoice', 'invoicing', 'excel', 'pdf'],   # Keywords users can search on pypi.org
  install_requires=['pandas', 'fpdf', 'openpyxl'],                 # Other 3rd-party libs that pip needs to install
  classifiers=[
    'Development Status :: 3 - Alpha',          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',          # Who is the audience for your library?
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Type a license again
    'Programming Language :: Python :: 3.8',      # Python versions that your library supports
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
  ],
)
