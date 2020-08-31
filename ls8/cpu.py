"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create the ram, registers and program-counter
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.checking = False
        self.pc = 0
        self.mar = 0
        self.flag = 0b00000000
        self.running = True

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    n = comment_split[0].strip()
                    if n == '':
                        continue
                    val = int(n, 2)
                    # store the val in ram
                    self.ram[address] = val

                    # increment the address
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]

        elif op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]

        elif op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]

        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]

        elif op == "CMP":
            
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001 
               
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
                
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
                
        # elif op == "NOT":
        #     self.reg[reg_a] ~= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # set Operations
        LDI = 130
        HLT = 1
        JMP = 84
        # Printing
        PRN = 71
        PRA = 72
        # Stack
        PUSH = 69
        POP = 70
        # Sub-Routines
        CALL = 80
        RET = 17
        # ALU
        ADD = 160
        SUB = 161
        MUL = 162
        DIV = 163
        MOD = 164
        OR = 170
        SHL = 172
        SHR = 173
        XOR = 171
        NOT = 105
        # Flags
        CMP = 167
        JEQ = 85
        JNE = 86
        # JGE = 90
        # JGT = 87
        # JLE = 89
        # JLT = 88

        # Stack Pointer (SP)
        SP = 7
        # set the SP to F2 or 243 on self.ram
        self.reg[SP] = 243

        while self.running:
            # Fetch
            ir = self.ram_read(self.pc)
            # Decode

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # op_size = 1
            op_size = ((ir >> 6) & 0b11) + 1
            # stop the loop
            self.checking = ((ir >> 4) & 0b1) == 1

            # loops thru if/elif checks and returns something
            if ir == LDI:  # HLT
                self.reg[operand_a] = operand_b

            elif ir == HLT:
                self.running = False

            elif ir == JMP:
                self.pc = self.reg[operand_a]
                

            # Flags
            elif ir == CMP:
                self.alu('CMP', operand_a, operand_b)
                
            elif ir == JEQ:
                if self.flag == 0b00000001:
                    self.pc = self.reg[operand_a]
                    
                else:
                    self.checking = False
            elif ir == JNE:
                
                if not self.flag & 0b00000001:
                    self.pc = self.reg[operand_a]
                    
                else:
                    self.checking = False
                
                    

            # elif ir == JGE:
            #     if self.flag == 1 or self.flag == 1:
            #         self.pc = self.reg[operand_a]
            #         op_size = 0

            # elif ir == JGT:
            #     if self.flag == 1:
            #         self.pc = self.reg[operand_a]
            #         op_size = 0

            # elif ir == JLE:
            #     if self.flag == 1 or self.flag == 1:
            #         self.pc = self.reg[operand_a]
            #         op_size = 0

            # elif ir == JLT:
            #     if self.flag == 1:
            #         self.pc = self.reg[operand_a]
            #         op_size = 0
            
        
            # Printing
            elif ir == PRN:
                print(self.reg[operand_a])
            elif ir == PRA:
                print(ord(self.reg[operand_a]))
            
            # ALU
            elif ir == SHL:
                self.alu('SHL', operand_a, operand_b)

            elif ir == SHR:
                self.alu('SHR', operand_a, operand_b)

            # elif ir == NOT:
            #     self.alu('NOT', operand_a, operand_b)

            elif ir == OR:
                self.alu('OR', operand_a, operand_b)

            elif ir == XOR:
                self.alu('XOR', operand_a, operand_b)

            elif ir == ADD:
                self.alu('ADD', operand_a, operand_b)

            elif ir == SUB:
                self.alu('SUB', operand_a, operand_b)

            elif ir == MUL:
                self.alu('MUL', operand_a, operand_b)

            elif ir == DIV:
                self.alu('DIV', operand_a, operand_b)
            
            elif ir == MOD:
                self.alu('MOD', operand_a, operand_b)

            
            # Call Stack
            elif ir == PUSH:
                # grab value fro the register
                val = self.reg[operand_a]

                # decrement Stack Pointer
                self.reg[SP] -= 1

                # add val to the stack
                self.ram[self.reg[SP]] = val

            elif ir == POP:
                # setup
                val = self.ram[self.reg[SP]]

                # take value from stack and put it in reg
                self.reg[operand_a] = val

                # increment the SP
                self.reg[SP] += 1

            # Sub-Routines
            elif ir == CALL:
                # push return address onto Stack
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2

                # set PC to the sub routines address
                self.pc = self.reg[operand_a]

                op_size = 0

            elif ir == RET:
                # POP returns from the stack the address for pc
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1

                op_size = 0

            
            if not self.checking:
                self.pc += op_size

    def ram_read(self, mar):
        """Read from the Ram"""
        # MAR
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        """Read / write from/to the Ram"""
        # MDR
        self.ram[mar] = mdr