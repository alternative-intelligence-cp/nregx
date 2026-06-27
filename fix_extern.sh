sed -i '/extern "nitpick_libc_sys" { func:npk_core_alloc/d' src/regex_vm.npk
sed -i '/extern "nitpick_libc_sys" { func:npk_core_dalloc/d' src/regex_vm.npk
