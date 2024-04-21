#include <nanobind/nanobind.h>

namespace nb = nanobind;

using namespace nb::literals;

NB_MODULE(pyethercat_ext, m) {
    m.def("add", [](int a, int b) { return a + b; }, "a"_a, "b"_a, "This function adds two numbers and increments if only one is provided.");
}