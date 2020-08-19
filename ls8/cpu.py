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
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 1
        ADD = 160
        SUB = 161
        MUL = 162
        DIV = 163

        isRunning = True

        while isRunning:
            # Fetch
            cmd = self.ram_read(self.pc)
            # Decode

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # op_size = 1
            op_size = ((cmd >> 6) & 0b11) + 1
            # alu_operations
            # alu_op = (cmd >> 5)

            # loops thru if/elif checks and returns something
            if cmd == LDI:  # HLT
                self.reg[operand_a] = operand_b
                # num_to_save = self.ram[operand_b]  # 300
                # reg_index = self.ram[operand_a]
                # self.reg[reg_index] = num_to_save

            elif cmd == PRN:
                print(self.reg[operand_a])
                # index_of_reg = self.ram[operand_a]
                # num_at_reg = self.reg[index_of_reg]
                # print(num_at_reg)
            elif cmd == HLT:
                isRunning = False
            elif cmd == ADD:
                self.alu('ADD', operand_a, operand_b)
                # a_reg_index = self.ram[operand_a]
                # b_reg_index = self.ram[operand_b]
                # self.reg[a_reg_index] += self.reg[b_reg_index]
            elif cmd == SUB:
                self.alu('SUB', operand_a, operand_b)
                # a_reg_index = self.ram[operand_a]
                # b_reg_index = self.ram[operand_b]
                # self.reg[a_reg_index] -= self.reg[b_reg_index]
            elif cmd == MUL:
                self.alu('MUL', operand_a, operand_b)
                # a_reg_index = self.ram[operand_a]
                # b_reg_index = self.ram[operand_b]
                # self.reg[a_reg_index] *= self.reg[b_reg_index]
            elif cmd == DIV:
                self.alu('DIV', operand_a, operand_b)
                # a_reg_index = self.ram[operand_a]
                # b_reg_index = self.ram[operand_b]
                # self.reg[a_reg_index] /= self.reg[b_reg_index]

            self.pc += op_size

    def ram_read(self, mar):
        """Read from the Ram"""
        # MAR
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        """Read / write from/to the Ram"""
        # MDR
        self.ram[mar] = mdr
