`timescale 1ns/1ps

module mult_tb ();

	parameter NUM_TEST = 1000;
	parameter DLY = 10;

	reg [3:0] A, B;
	reg [7:0] P_CORRECT;
	wire [7:0] ui_in, uio_in, uio_out, uio_oe;
	reg ena, clk, rst_n;

	wire [7:0] P;
	wire true;
	integer i, pass;	

	tt_um_mult_top TT_MULT (.ui_in(ui_in), .uo_out(P), .uio_in(uio_in), .uio_out(uio_out), .uio_oe(uio_oe), .ena(ena), .clk(clk), .rst_n(rst_n));


	assign ui_in = {A,B};
	assign uio_in = {8{1'b0}};


	assign true = (P == P_CORRECT);	

	always @(i) begin
		if(ena)begin
			P_CORRECT = A * B;	

			if (true==1)
				pass = pass + 1;
		end
		else begin
			P_CORRECT = 0;	

			if (true==1)
				pass = pass + 1;

		end
				
		
	end

	always #(DLY/2) clk = ~clk;


	initial begin
		i = 0;
		pass = 0;
		clk = 1'b1;
		A = 4'h1;
		B = 4'h2;
		rst_n = 1'b0;
		ena = 1'b0;
	

		#DLY
		rst_n = 1'b1;
		
		#DLY
		ena = 1'b1;
		i = i + 1;

		for (i = 1; i < NUM_TEST; i = i + 1) begin
			#(DLY)
			A	= $random;
			B	= $random;
		end

		#DLY
		i = i + 1;

		#DLY

		$display ("**** FINISH ***");
		$display ("MULT passes %g out of %g tests",pass,i);
		$stop;

/////// End of Verification 
	
	end

endmodule

