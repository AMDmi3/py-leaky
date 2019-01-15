/*
 * Copyright (c) 2019 Dmitry Marakasov <amdmi3@amdmi3.ru>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <Python.h>

#include <stdlib.h>

static PyObject* no_leak(PyObject *self, PyObject *args) {
	(void)self; // (unused)
	(void)args; // (unused)

	Py_RETURN_NONE;
}

static PyObject* leak_int(PyObject *self, PyObject *args) {
	(void)self; // (unused)
	(void)args; // (unused)

	PyLong_FromLong(0x876543210);

	Py_RETURN_NONE;
}

static PyObject* doublefree_int(PyObject *self, PyObject *args) {
	(void)self; // (unused)
	(void)args; // (unused)

	PyObject* o = PyLong_FromLong(0x876543210);
	Py_DECREF(o);
	Py_DECREF(o);

	Py_RETURN_NONE;
}

static PyObject* leak_malloc(PyObject *self, PyObject *args) {
	(void)self; // (unused)
	(void)args; // (unused)

	(void)malloc(1024);

	Py_RETURN_NONE;
}

static PyObject* doublefree_malloc(PyObject *self, PyObject *args) {
	(void)self; // (unused)
	(void)args; // (unused)

	void* p = malloc(1024);
	free(p);
	free(p);

	Py_RETURN_NONE;
}

static PyMethodDef module_methods[] = {
	{"no_leak", (PyCFunction)no_leak, METH_VARARGS, ""},
	{"leak_int", (PyCFunction)leak_int, METH_VARARGS, ""},
	{"doublefree_int", (PyCFunction)doublefree_int, METH_VARARGS, ""},
	{"leak_malloc", (PyCFunction)leak_malloc, METH_VARARGS, ""},
	{"doublefree_malloc", (PyCFunction)doublefree_malloc, METH_VARARGS, ""},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_definition = {
	PyModuleDef_HEAD_INIT,
	"leaky",
	"leaky module",
	-1,
	module_methods, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_leaky(void) {
	return PyModule_Create(&module_definition);
}
