/* Copyright (C) European XFEL GmbH Schenefeld. All rights reserved.
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/. */

#define PY_SSIZE_T_CLEAN
//#define Py_LIMITED_API 0x030B0000

#include <stdlib.h>
#include <Python.h>
#include "zlib.h"

#define DEF_MEM_LEVEL 8

// malloc & free functions copied from CPython
static void*
PyZlib_Malloc(voidpf ctx, uInt items, uInt size)
{
    if (size != 0 && items > (size_t)PY_SSIZE_T_MAX / size)
        return NULL;
    /* PyMem_Malloc() cannot be used: the GIL is not held when
       inflate() and deflate() are called */
    return PyMem_RawMalloc((size_t)items * (size_t)size);
}

static void
PyZlib_Free(voidpf ctx, void *ptr)
{
    PyMem_RawFree(ptr);
}

// zlib_error copied from CPython
static void
zlib_error(z_stream zst, int err, const char *msg)
{
    const char *zmsg = Z_NULL;
    /* In case of a version mismatch, zst.msg won't be initialized.
       Check for this case first, before looking at zst.msg. */
    if (err == Z_VERSION_ERROR)
        zmsg = "library version mismatch";
    if (zmsg == Z_NULL)
        zmsg = zst.msg;
    if (zmsg == Z_NULL) {
        switch (err) {
        case Z_BUF_ERROR:
            zmsg = "incomplete or truncated stream";
            break;
        case Z_STREAM_ERROR:
            zmsg = "inconsistent stream state";
            break;
        case Z_DATA_ERROR:
            zmsg = "invalid input data";
            break;
        }
    }
    if (zmsg == Z_NULL)
        PyErr_Format(PyExc_RuntimeError, "Error %d %s", err, msg);
    else
        PyErr_Format(PyExc_RuntimeError, "Error %d %s: %.200s", err, msg, zmsg);
}

static PyObject *
compress_into(PyObject *module, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"data", "output", "level", "wbits", NULL};
    PyObject *return_value = NULL;
    Py_ssize_t bytes_written;
    Py_buffer input, output;
    int level=Z_DEFAULT_COMPRESSION, wbits=MAX_WBITS;
    z_stream zst;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*w*|ii", keywords,
                                     &input, &output, &level, &wbits)) {
        return NULL;
    }

    zst.opaque = NULL;
    zst.zalloc = PyZlib_Malloc;
    zst.zfree = PyZlib_Free;
    zst.next_in = input.buf;
    zst.avail_in = input.len;
    zst.next_out = output.buf;
    zst.avail_out = output.len;
    int err = deflateInit2(&zst, level, Z_DEFLATED, wbits, DEF_MEM_LEVEL,
                           Z_DEFAULT_STRATEGY);

    switch (err) {
    case Z_OK:
        break;
    case Z_MEM_ERROR:
        PyErr_SetString(PyExc_MemoryError,
                        "Out of memory while compressing data");
        goto done;
    case Z_STREAM_ERROR:
        PyErr_SetString(PyExc_ValueError, "Bad compression level");
        goto done;
    default:
        deflateEnd(&zst);
        zlib_error(zst, err, "while preparing to compress data");
        goto done;
    }

    Py_BEGIN_ALLOW_THREADS
    err = deflate(&zst, Z_FINISH);
    Py_END_ALLOW_THREADS

    switch (err) {
        case Z_STREAM_END:
            break;
        case Z_OK:
        case Z_BUF_ERROR:
            deflateEnd(&zst);
            PyErr_SetString(PyExc_ValueError, "Not enough space in output buffer");
            goto done;
        default:
            deflateEnd(&zst);
            zlib_error(zst, err, "while compressing data");
            goto done;
    }
    bytes_written = output.len - zst.avail_out;
    err = deflateEnd(&zst);
    if (err != Z_OK) {
        zlib_error(zst, err, "while finishing compression");
        goto done;
    }

    return_value = PyLong_FromSsize_t(bytes_written);

    done:
      PyBuffer_Release(&input);
      PyBuffer_Release(&output);
      return return_value;
}


static PyObject *
decompress_into(PyObject *module, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"data", "output", "wbits", NULL};
    PyObject *return_value = NULL;
    Py_ssize_t bytes_written;
    Py_buffer input, output;
    int wbits=MAX_WBITS;
    z_stream zst;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*w*|i", keywords,
                                     &input, &output, &wbits)) {
        return NULL;
    }

    zst.opaque = NULL;
    zst.zalloc = PyZlib_Malloc;
    zst.zfree = PyZlib_Free;
    zst.next_in = input.buf;
    zst.avail_in = input.len;
    zst.next_out = output.buf;
    zst.avail_out = output.len;
    int err = inflateInit2(&zst, wbits);

    switch (err) {
    case Z_OK:
        break;
    case Z_MEM_ERROR:
        PyErr_SetString(PyExc_MemoryError,
                        "Out of memory while decompressing data");
        goto done;
    default:
        inflateEnd(&zst);
        zlib_error(zst, err, "while preparing to decompress data");
        goto done;
    }

    Py_BEGIN_ALLOW_THREADS
    err = inflate(&zst, Z_FINISH);
    Py_END_ALLOW_THREADS

    switch (err) {
        case Z_STREAM_END:
            break;
        case Z_OK:
        case Z_BUF_ERROR:
            inflateEnd(&zst);
            PyErr_SetString(PyExc_ValueError, "Not enough space in output buffer");
            goto done;
        default:
            inflateEnd(&zst);
            zlib_error(zst, err, "while decompressing data");
            goto done;
    }
    bytes_written = output.len - zst.avail_out;

    err = inflateEnd(&zst);
    if (err != Z_OK) {
        zlib_error(zst, err, "while finishing decompression");
        goto done;
    }

    return_value = PyLong_FromSsize_t(bytes_written);

    done:
      PyBuffer_Release(&input);
      PyBuffer_Release(&output);
      return return_value;
}


inline void shuffle_core(Py_buffer input, Py_buffer output, ssize_t itemsize) {
    ssize_t n_entries, i, j;
    char *outp = (char *)output.buf, *inp = (char *)input.buf;
    n_entries = input.len / itemsize;
    for (i = 0; i < n_entries; i++) {
        for (j = 0; j < itemsize; j++) {
            outp[(j * n_entries) + i] = inp[(i * itemsize) + j];
        }
    }
}

static PyObject *
shuffle(PyObject *module, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"data", "output", "itemsize", NULL};
    PyObject *return_value = NULL;
    Py_ssize_t itemsize;
    Py_buffer input, output;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*w*n", keywords,
                                     &input, &output, &itemsize)) {
        return NULL;
    }

    if (input.len != output.len) {
        PyErr_SetString(PyExc_ValueError,
                        "input & output buffers are different sizes");
        goto done;
    }
    if (itemsize > 0 && ((input.len % itemsize) != 0)) {
        PyErr_Format(
            PyExc_ValueError,
            "buffer size (%zd) is not a multiple of itemsize (%zd)",
            input.len, itemsize
        );
        goto done;
    }

    // This switch allows for compiler optimisations; see note in unshuffle
    switch (itemsize) {
        case 2:
          Py_BEGIN_ALLOW_THREADS
          shuffle_core(input, output, 2);
          Py_END_ALLOW_THREADS
          break;
        case 4:
          Py_BEGIN_ALLOW_THREADS
          shuffle_core(input, output, 4);
          Py_END_ALLOW_THREADS
          break;
        case 8:
          Py_BEGIN_ALLOW_THREADS
          shuffle_core(input, output, 8);
          Py_END_ALLOW_THREADS
          break;
        default:
          PyErr_SetString(PyExc_ValueError, "itemsize must be 2, 4, or 8");
          goto done;
    }

    return_value = Py_NewRef(Py_None);  // Success

    done:
      PyBuffer_Release(&input);
      PyBuffer_Release(&output);
      return return_value;
}


inline void unshuffle_core(Py_buffer input, Py_buffer output, ssize_t itemsize) {
    ssize_t n_entries, i, j;
    char *outp = (char *)output.buf, *inp = (char *)input.buf;
    n_entries = input.len / itemsize;
    for (i = 0; i < n_entries; i++) {
        for (j = 0; j < itemsize; j++) {
            outp[(i * itemsize) + j] = inp[(j * n_entries) + i];
        }
    }
}

static PyObject *
unshuffle(PyObject *module, PyObject *args, PyObject *kwargs) {
    static char *keywords[] = {"data", "output", "itemsize", NULL};
    PyObject *return_value = NULL;
    Py_ssize_t itemsize;
    Py_buffer input, output;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "y*w*n", keywords,
                                     &input, &output, &itemsize)) {
        return NULL;
    }
    
    if (input.len != output.len) {
        PyErr_SetString(PyExc_ValueError,
                        "input & output buffers are different sizes");
        goto done;
    }
    if (itemsize > 0 && ((input.len % itemsize) != 0)) {
        PyErr_Format(
            PyExc_ValueError,
            "buffer size (%zd) is not a multiple of itemsize (%zd)",
            input.len, itemsize
        );
        goto done;
    }

    // -O3 optimisations with the inline function and a known size for the
    // inner loop make this about 10x faster than calling with an arbitrary
    // itemsize (tested with itemsize=4). We're only expecting to unshuffle
    // 2, 4, or 8 bytes, so no fallback is provided for now.
    switch (itemsize) {
        case 2:
          Py_BEGIN_ALLOW_THREADS
          unshuffle_core(input, output, 2);
          Py_END_ALLOW_THREADS
          break;
        case 4:
          Py_BEGIN_ALLOW_THREADS
          unshuffle_core(input, output, 4);
          Py_END_ALLOW_THREADS
          break;
        case 8:
          Py_BEGIN_ALLOW_THREADS
          unshuffle_core(input, output, 8);
          Py_END_ALLOW_THREADS
          break;
        default:
          PyErr_SetString(PyExc_ValueError, "itemsize must be 2, 4, or 8");
          goto done;
    }

    return_value = Py_NewRef(Py_None);  // Success

    done:
      PyBuffer_Release(&input);
      PyBuffer_Release(&output);
      return return_value;
}


static PyMethodDef ZlibIntoMethods[] = {
    {"compress_into", (PyCFunction)compress_into, METH_VARARGS | METH_KEYWORDS, "zlib compress data into a buffer"},
    {"decompress_into", (PyCFunction)decompress_into, METH_VARARGS | METH_KEYWORDS, "zlib decompress data into a buffer"},
    {"shuffle", (PyCFunction)shuffle, METH_VARARGS | METH_KEYWORDS, "byte-shuffle data, allowing for better compression"},
    {"unshuffle", (PyCFunction)unshuffle, METH_VARARGS | METH_KEYWORDS, "byte-unshuffle data, typically after decompression"},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef_Slot zlib_into_slots[] = {
#ifdef Py_GIL_DISABLED
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
    {0, NULL}
};

static struct PyModuleDef zlibintomodule = {
    PyModuleDef_HEAD_INIT,
    "zlib_into",
    NULL,  // docstring
    0,
    ZlibIntoMethods,
    zlib_into_slots,
};

PyMODINIT_FUNC
PyInit_zlib_into(void) {
    return PyModuleDef_Init(&zlibintomodule);
}
