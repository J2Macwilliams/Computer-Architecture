"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create the ram, registers and program-counter
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.mar = 0
        self.running = True
        

    def load(self):
        """Load a program into memory."""

        address = 0


        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            # loads the ram with instructions
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # set variables
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        isRunning = True

        
        while isRunning:
            # Fetch
            cmd = self.ram_read(self.pc)
            # Decode
            
            # operand a
            operand_a = self.pc + 1
            # operand b
            operand_b = self.pc + 2
            
            op_size = 1

            # loops thru if/elif checks and returns something
            if cmd == LDI: #HLT
                item = self.ram_read(operand_b)
                self.reg[self.mar] = item
                op_size = 3
            elif cmd == PRN:
                found = self.reg[self.mar]
                print(found)
                op_size = 2
            elif cmd == HLT:
                isRunning = False
                op_size = 1

            self.pc += op_size
        

    def ram_read(self, mar):
        """Read from the Ram"""
        # MAR
        return self.ram[mar]
        
        

    def ram_write(self, mar, mdr):
        """Read / write from/to the Ram"""
        # MDR
        self.ram[mar] = mdr