#!/usr/bin/env python

"""Setup linked packages required for GGRC
"""

import subprocess

def run_shell(script):
  proc = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE)
  proc.wait()
  return proc.returncode, proc.stdout.read()

def ln_package(source, target, force=True):
  force = "-f" if force else ""
  command = "ln %s -s %s %s" % (force, source, target)
  if source.startswith(target):
    print("Skipping possible self-link of %s" % (source,))
  else:
    print(command)
    return subprocess.call(command, shell=True)

def _run_system_python_script_output(script, unindent=None):
  # Unindent and escape script
  script_lines = script.lstrip('\n').rstrip().splitlines()
  script_lines = map(lambda line: line[unindent:], script_lines)
  script = "\\n".join(script_lines)

  script = """%(python_path)s -c 'exec("%(script)s")'""" % {
    'python_path': "/usr/bin/python",
    'script': script,
    }

  return_code, result = run_shell(script)
  if return_code == 0:
    if len(result.strip()) > 0:
      return result.strip()
    else:
      return None
  else:
    return None

def _get_system_python_import_path(module, path_getter):
  python_path = "/usr/bin/python"

  script = """
    try:
      import %(module)s
      print(%(path_getter)s)
    except ImportError, e:
      print ""
  """ % {
    'module': module,
    'path_getter': path_getter
    }

  return _run_system_python_script_output(script, unindent=4)


def setup_mysql_packages(packages_dir):
  """
  This links MySQLdb module to opt/packages for use inside
  the otherwise-isolated virtual environment
  """
  module_path = _get_system_python_import_path('MySQLdb', 'MySQLdb.__path__[0]')
  if module_path:
    ln_package(module_path, packages_dir)
  else:
    print("Failed to import MySQLdb -- ensure it is available")

  module_path = _get_system_python_import_path('_mysql', '_mysql.__file__')
  if module_path:
    ln_package(module_path, packages_dir)
  else:
    print("Failed to import _mysql -- ensure it is available")

  module_path = _get_system_python_import_path('_mysql_exceptions', '_mysql_exceptions.__file__')
  if module_path:
    ln_package(module_path, packages_dir)
  else:
    print("Failed to import _mysql_exceptions -- ensure it is available")

def setup_imaging_packages(packages_dir):
  module_path = _get_system_python_import_path('PIL', 'PIL.__path__[0]')
  if module_path:
    ln_package(module_path, packages_dir)
  else:
    print("Failed to import PIL -- ensure it is available")

def setup_google_packages(opt_dir, packages_dir):
  """
  This links the `google` package from google_appengine
  to opt/packages for use inside the virtual environment
  """
  try:
    import google
    google_path = google.__path__[0]
  except ImportError as e:
    google_path = "%s/google_appengine/google" % (opt_dir,)

  ln_package(google_path, packages_dir)

def main(packages_dir):
  command = "mkdir -p {packages_dir}".format(packages_dir=packages_dir)
  print(command)
  subprocess.call(command, shell=True)
  setup_mysql_packages(packages_dir)
  setup_imaging_packages(packages_dir)

if __name__ == '__main__':
  import sys
  main(sys.argv[1].strip())
