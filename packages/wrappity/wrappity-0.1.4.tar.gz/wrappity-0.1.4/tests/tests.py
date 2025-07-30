from wrappity import Wrapper, inspect, unwrap, wrap

test_obj = {"a": 1, "b": [1, 2, 3], "c": {"d": 4}}
wrapped_obj = wrap(test_obj)


def test_wrap_unwrap():
	# test wrapping and unwrapping
	assert isinstance(wrapped_obj, Wrapper)
	unwrapped_obj = unwrap(wrapped_obj)
	assert test_obj == unwrapped_obj


def test_inspect():
	# test inspecting
	paths = inspect(wrapped_obj)
	assert paths == ["a=1", "b[0]=1", "b[1]=2", "b[2]=3", "c.d=4"]


def test_underscore_access():
	# test underscore access
	assert wrapped_obj.a._ == 1
	assert wrapped_obj.b[1]._ == 2
	assert wrapped_obj.c.d._ == 4


def test_access_miss():
	# test access miss
	assert bool(wrapped_obj.e) is False
	assert wrapped_obj.e._ is None


def test_missed_access_hook():
	# test missed access hook
	def missed_access_callable(object_, what, access_type):
		assert object_ == wrapped_obj
		assert what == "e"
		assert access_type == Wrapper.ACCESS_TYPE_DICT

	wrapped_obj = wrap(test_obj, missed_access_hook=missed_access_callable)
	wrapped_obj.e


def test_inspect_show_values_true():
	# test inspecting with show_values=True
	paths = inspect(wrapped_obj, show_values=True)
	assert paths == ["a=1", "b[0]=1", "b[1]=2", "b[2]=3", "c.d=4"]


def test_inspect_show_values_false():
	# test inspecting with show_values=False
	paths = inspect(wrapped_obj, show_values=False)
	assert paths == ["a", "b[0]", "b[1]", "b[2]", "c.d"]


def test_ensure_list_on_none():
	# test _ensure_list on None
	assert wrapped_obj.e._el()._ == []


def test_ensure_list_on_existing_list():
    # test _ensure_list on existing list returns the same list
    wrapped_obj.b._el()
    assert isinstance(wrapped_obj.b._, list)
    assert wrapped_obj.b._ == [1, 2, 3]


def test_underscore_unwraps_nested_structure():
    # test underscore unwraps nested structure
    assert type(wrapped_obj.c._['d']) is int
    assert wrapped_obj.c._['d'] == 4