from typing import Any, Callable


class Wrapper(object):
	ACCESS_TYPE_DICT = "access_type_dict"
	ACCESS_TYPE_LIST = "access_type_list"

	def __init__(
		self, object_: Any = None, attr_translations: dict | None = None, missed_access_hook: Callable = None
	):
		self._wrapped_object = object_
		self._attr_translations = attr_translations or {}
		self._missed_access_hook = missed_access_hook

	def __create_new__(self, object_=None):
		return Wrapper(object_, attr_translations=self._attr_translations, missed_access_hook=self._missed_access_hook)

	def _ensure_list(self):
		if not isinstance(self._wrapped_object,list):
			# ensure we're not unnecessarily filling the list with None
			if self._wrapped_object is None:
				self._wrapped_object = []
			else:
				self._wrapped_object = [self.__create_new__(self._wrapped_object)]
		return self

	def _el(self):
		# alias for _ensure_list
		return self._ensure_list()

	def __getattr__(self, attr_name):
		if attr_name == "_":
			return unwrap(self)
		if attr_name.startswith("_") and len(attr_name) > 2 and attr_name[1] != "_":  # apply translations if necessary
			attr_name = attr_name[1:]
			for translation_key, translation_value in self._attr_translations.items():
				if attr_name.startswith(translation_key):
					attr_name = attr_name.replace(translation_key, translation_value)
					break
		if isinstance(self._wrapped_object,dict):
			if attr_name in self._wrapped_object:
				return self._wrapped_object.get(attr_name)
			else:
				if callable(self._missed_access_hook):
					self._missed_access_hook(object_=self, what=attr_name, access_type=Wrapper.ACCESS_TYPE_DICT)
				return self.__create_new__()
		# access miss
		if callable(self._missed_access_hook):
			self._missed_access_hook(object_=self, what=attr_name, access_type=Wrapper.ACCESS_TYPE_DICT)
		return self.__create_new__()

	def __getitem__(self, index):
		if isinstance(self._wrapped_object,list):
			if index < len(self._wrapped_object):
				return self._wrapped_object[index]
			else:
				if callable(self._missed_access_hook):
					self._missed_access_hook(object_=self, what=index, access_type=Wrapper.ACCESS_TYPE_LIST)
				return self.__create_new__()
		# access miss
		if callable(self._missed_access_hook):
			self._missed_access_hook(object_=self, what=index, access_type=Wrapper.ACCESS_TYPE_LIST)
		return self.__create_new__()

	def __bool__(self):
		return False if self._wrapped_object is None else bool(self._wrapped_object)

	def __iter__(self):
		if isinstance(self._wrapped_object,list) or isinstance(self._wrapped_object,tuple) or isinstance(self._wrapped_object,dict):
			yield from self._wrapped_object

	def __len__(self):
		return len(self._wrapped_object) if isinstance(self._wrapped_object,list) or isinstance(self._wrapped_object,tuple) or isinstance(self._wrapped_object,dict) else 0

	def items(self):
		return self._wrapped_object.items() if isinstance(self._wrapped_object,list) or isinstance(self._wrapped_object,tuple) or isinstance(self._wrapped_object,dict) else []

	def values(self):
		return self._wrapped_object.values() if isinstance(self._wrapped_object,list) or isinstance(self._wrapped_object,tuple) or isinstance(self._wrapped_object,dict) else []

	def keys(self):
		return self._wrapped_object.keys() if isinstance(self._wrapped_object,list) or isinstance(self._wrapped_object,tuple) or isinstance(self._wrapped_object,dict) else []

	def __repr__(self):
		return f"wrapped({type(self._wrapped_object)}): {self._wrapped_object}"

	def __str__(self):
		return str(self._wrapped_object) if self._wrapped_object is not None else ""


def wrap(object_: Any, attr_translations: dict = {}, missed_access_hook: Callable = None) -> Wrapper:
	"""Wraps an object in a Wrapper instance, proceeding recursively if necessary

	Args:
					object_ (Any): the object to wrap
					attr_translations (dict, optional): Any attribute name translations required to access subobjects which have names that are not valid names in Python.
					missed_access_hook (Callable, optional): An optional function that gets called when there's a attempt to access a subobject that does not exist.

	Returns:
					Wrapper: the original object wrapped in a Wrapper instance
	"""
	if isinstance(object_,dict):
		return Wrapper(
			{
				k: wrap(v, attr_translations=attr_translations, missed_access_hook=missed_access_hook)
				for k, v in object_.items()
			},
			attr_translations=attr_translations,
			missed_access_hook=missed_access_hook,
		)
	elif isinstance(object_,list) or isinstance(object_,tuple):
		return Wrapper(
			[wrap(i, attr_translations=attr_translations, missed_access_hook=missed_access_hook) for i in object_],
			attr_translations=attr_translations,
			missed_access_hook=missed_access_hook,
		)
	else:
		return Wrapper(
			object_,
			attr_translations=attr_translations,
			missed_access_hook=missed_access_hook,
		)


def unwrap(object_: Wrapper) -> Any:
	"""Unwraps a previously wrapped object, proceeding recursively if necessary

	Args:
					object_ (Wrapper): the wrapped object to unwrap

	Returns:
					Any: the unwrapped object
	"""
	if type(object_) != Wrapper:
		return object_  # nothing to unwrap
	if isinstance(object_._wrapped_object,dict):
		return {k: unwrap(v) for k, v in object_._wrapped_object.items()}
	elif isinstance(object_._wrapped_object,list) or isinstance(object_._wrapped_object,tuple):
		return [unwrap(i) for i in object_._wrapped_object]
	else:
		return object_._wrapped_object


def inspect(object_: Wrapper, show_values: bool = True) -> list[str]:
	"""Inspects the wrapped object (recursively if needed) and returns a list of paths to all leaf nodes

	Args:
			object_ (Wrapper): a wrapped object
			show_values (bool, optional): whether to include the leaf values in the paths

	Returns:
			list[str]: list of paths to all leaf nodes
	"""

	def find_paths(object_, current_path=None):
		if current_path is None:
			current_path = []
		if type(object_) != Wrapper:  # Leaf node
			yield current_path + [object_]
		elif isinstance(object_._wrapped_object,dict):
			for key, value in object_._wrapped_object.items():
				yield from find_paths(value, current_path + [key])
		elif isinstance(object_._wrapped_object,list) or isinstance(object_._wrapped_object,tuple):
			for index, value in enumerate(object_._wrapped_object):
				yield from find_paths(value, current_path + [f"[{index}]"])
		else:
			yield current_path + [object_]

	return [
		(".".join(map(str, path[:-1]))).replace(".[", "[") + (f"={path[-1]}" if show_values else "")
		for path in find_paths(object_)
	]

def print_inspect(object_: Wrapper, show_values: bool = True):
    """Prints the paths to all leaf nodes of the wrapped object

    Args:
            object_ (Wrapper): a wrapped object
            show_values (bool, optional): whether to include the leaf values in the paths
    """
    for path in inspect(object_, show_values=show_values):
        print(path)