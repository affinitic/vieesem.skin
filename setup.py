from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='vieesem.skin',
      version=version,
      description="Theme package for VIEESEM website",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Affinitic',
      author='Affinitic',
      author_email='info@affinitic.be',
      url='https://github.com/affinitic/vieesem.skin',
      license='gpl',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['vieesem'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.api',
          'plone.app.theming',
          'plone.app.themingplugins',
          'plone.resource',
          'Products.AddRemoveWidget',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
