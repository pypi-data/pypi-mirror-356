
import os
import sys

from jennifer.agent.class_selector import wrap_class_instance_method, wrap_non_instance_method, MethodSelector


def add_profile_global_func(module_name, func_name):
    try:
        module_obj = sys.modules[module_name]
        target_func = getattr(module_obj, func_name)
        if target_func is None:
            return

        target_func_name = str(target_func)
        if target_func_name.find('wrap_non_instance_method') != -1:
            return

        hook_info = {
            'param_mode': MethodSelector.NO_PARAMETER,
            'arg_idx': None,
            'arg_names': None,
        }

        profile_info = {
            'original_target_container': module_obj,
            'profile_type': MethodSelector.PROFILE_METHOD,
            'original_func': target_func,
            'func_type': MethodSelector.MODULE_FUNCTION,
            'profile_func_key': func_name,
            'fqdn': module_obj.__name__ + ' .' + func_name,
            MethodSelector.PROFILE_METHOD: hook_info,
        }

        wrapped_func = wrap_non_instance_method(target_func, profile_info)
        setattr(module_obj, func_name, wrapped_func)
    except Exception as e:
        print(os.getpid(), '[jennifer.user_method]', e)


def add_profile_class_method(class_obj, func_name):
    try:
        target_func = getattr(class_obj, func_name)
        if target_func is None:
            return

        target_func_name = str(target_func)
        if target_func_name.find('wrap_class_instance_method') != -1:
            return

        hook_info = {
            'param_mode': MethodSelector.NO_PARAMETER,
            'arg_idx': None,
            'arg_names': None,
        }

        profile_info = {
            'original_target_container': class_obj,
            'profile_type': MethodSelector.PROFILE_SERVICE,
            'original_func': target_func,
            'func_type': MethodSelector.CLASS_INSTANCE_METHOD,
            'profile_func_key': func_name,
            'fqdn': class_obj.__name__ + '.' + func_name,
            MethodSelector.PROFILE_SERVICE: hook_info,
        }

        wrapped_func = wrap_class_instance_method(target_func, profile_info)
        setattr(class_obj, func_name, wrapped_func)
    except Exception as e:
        print(os.getpid(), '[jennifer.user_service]', e)
