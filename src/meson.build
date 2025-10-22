pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'flippybit'

gnome = import('gnome')

# Compile UI resources
gnome.compile_resources('flippybit',
  'flippybit.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

# Create configuration for the launcher script
conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('pkgdatadir', pkgdatadir)

# Generate the launcher script
configure_file(
  input: 'flippybit.in',
  output: 'flippybit',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

# Install all Python files and directories
install_data(
  ['main.py', '__init__.py'],
  install_dir: moduledir
)

# Install all subdirectories
install_subdir('ui',
  install_dir: moduledir,
  exclude_directories: ['__pycache__']
)

install_subdir('core',
  install_dir: moduledir,
  exclude_directories: ['__pycache__']
)

install_subdir('models',
  install_dir: moduledir,
  exclude_directories: ['__pycache__']
)

install_subdir('views',
  install_dir: moduledir,
  exclude_directories: ['__pycache__']
)