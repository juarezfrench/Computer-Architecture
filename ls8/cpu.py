"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        # self.ir = 0 # Instruction Register
        # self.mar = 0 # Memory Address Register
        # self.mdr = 0 # Memory Data Register   
        self.running = True
        self.instructions = {
            0b10000010: self.handle_LDI,
            0b01000111: self.handle_PRN,
            0b00000001: self.handle_HLT,
            0b10100010: self.handle_MUL
        }    

    def load(self):
        """Load a program into memory."""

        # self.mar = 0
        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    # split before comment
                    comment_split = line.split('#')

                    # convert to a number splitting and stripping
                    num = comment_split[0].strip()

                    if num == '':
                        continue  # ignore blank lines
                    
                    val = int(num, 2)
                    
                    # store val in memory at the given address
                    self.ram[address] = val

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)
       

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
            while self.mar < len(program):
                self.mdr = program[self.mar]
                self.ram_write(self.mdr, self.mar)
                self.mar += 1



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
        # print("running")
        self.running = True

    def handle_HLT(self, ops):
        self.running = False

    def handle_LDI(self, ops):
        self.mar = self.ram_read(self.pc + 1)
        self.mdr = self.ram_read(self.pc + 2)
        
    def handle_PRN(self, ops):
        self.mar = self.ram_read(self.pc + 1)  
    
    def ram_read(self, memory_address):
        return self.ram[memory_address]

    def ram_write(self, memory_data, memory_address):
        self.ram[memory_address] = memory_data      


newCPU = CPU()

newCPU.run()

