mov dword ptr ds:[rf_ptr_eax_save], eax
mov al, byte ptr ds:[redir_flag]
test al, al
jnz shader_loop
jmp execute_stolen
exit_restore:
    push 0
    mov eax, dword ptr ds:[pglUseProgram]
    mov eax, dword ptr ds:[eax]
    call eax
    xor eax, eax
    call GfxTarget
    mov ebx, dword ptr ds:[rf_ptr_ebx_save]
    mov edx, dword ptr ds:[rf_ptr_edx_save]
    mov ebp, dword ptr ds:[rf_ptr_ebp_save]
    mov esp, dword ptr ds:[rf_ptr_esp_save]
    mov esi, dword ptr ds:[rf_ptr_esi_save]
    mov edi, dword ptr ds:[rf_ptr_edi_save]
execute_stolen:
    mov eax, dword ptr ds:[rf_ptr_eax_save]
    lea edx, ss:[ebp-0x493C]
    jmp RFhookContinue
shader_loop:
    mov dword ptr ds:[rf_ptr_ebx_save], ebx
    mov dword ptr ds:[rf_ptr_edx_save], edx
    mov dword ptr ds:[rf_ptr_ebp_save], ebp
    mov dword ptr ds:[rf_ptr_esp_save], esp
    mov dword ptr ds:[rf_ptr_esi_save], esi
    mov dword ptr ds:[rf_ptr_edi_save], edi

    mov edi, dword ptr ds:[shader_list_ptr]
iterate_next:
    mov eax, dword ptr ds:[edi]
    test eax, eax
    jz exit_restore
    mov esi, edi
    push eax
    mov eax, dword ptr ds:[pglUseProgram]
    mov eax, dword ptr ds:[eax]
    call eax
    push 0x84c0
    mov eax, dword ptr ds:[pglActiveTexture]
    mov eax, dword ptr ds:[eax]
    call eax
    mov eax, dword ptr ds:[pRenderTarget]
    push eax
    push 0xde1
    mov eax, dword ptr ds:[pglBindTexture]
    mov eax, dword ptr ds:[eax]
    call eax
    mov eax, dword ptr ds:[uniformScreenTexture]
    push eax
    mov eax, dword ptr ds:[esi]
    push eax
    mov eax, dword ptr ds:[pglGetUniformLocation]
    mov eax, dword ptr ds:[eax]
    call eax
    push 0
    push eax
    mov eax, dword ptr ds:[pglUniform1i]
    mov eax, dword ptr ds:[eax]
    call eax
    add edi, 0x4
    jmp iterate_next