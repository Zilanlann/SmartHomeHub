@REM This batch file has been generated by the IAR Embedded Workbench
@REM C-SPY Debugger, as an aid to preparing a command line for running
@REM the cspybat command line utility using the appropriate settings.
@REM
@REM You can launch cspybat by typing the name of this batch file followed
@REM by the name of the debug file (usually an ELF/DWARF or UBROF file).
@REM Note that this file is generated every time a new debug session
@REM is initialized, so you may want to move or rename the file before
@REM making changes.
@REM 


"D:\Program Files\IAR Systems\Embedded Workbench 6.0 Evaluation\common\bin\cspybat" "D:\Program Files\IAR Systems\Embedded Workbench 6.0 Evaluation\8051\bin\8051proc.dll" "D:\Program Files\IAR Systems\Embedded Workbench 6.0 Evaluation\8051\bin\8051emu_cc.dll"  %1 --plugin "D:\Program Files\IAR Systems\Embedded Workbench 6.0 Evaluation\8051\bin\8051bat.dll" --backend -B "--proc_core" "plain" "--proc_code_model" "near" "--proc_nr_virtual_regs" "8" "--proc_pdata_bank_reg_addr" "0x93" "--proc_dptr_nr_of" "1" "--proc_data_model" "large" "-p" "D:\Program Files\IAR Systems\Embedded Workbench 6.0 Evaluation\8051\config\devices\_generic\io8051.ddf" "--proc_exclude_exit_breakpoint" "--proc_driver" "chipcon" "--retain_memory" "--verify_download" "use_crc16" "--stack_overflow" "--number_of_banks" "4" 


