from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
  def initialize(self, version, build_data):
    print("YAY WE HAVE BUILD HOOKS")
