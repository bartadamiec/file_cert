from fpdf import FPDF

def report_generator_service(filename: str, results: list[dict]):
    class VerificationReport(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)
            self.cell(0, 10, 'Validation Report of Electronical Sign', 0, 1, 'C')
            self.ln(10)

        def add_result(self, result):
            self.set_font('Arial', '', 12)

            self.cell(0, 10, f"Signed by {result['signer']}", 0, 1)
            self.cell(0, 10, f"Status: {'Valid' if result['valid'] else 'Invalid'}", 0, 1)
            self.cell(0, 10, f"Wasn't changed after signing" if result['intact'] else 'Was changed after signing', 0, 1)
            self.cell(0, 10, f"Sign date: {result['signing_time']}", 0, 1)
            self.cell(0, 10, f"Validation date: {result['validation_time']}", 0, 1)
            self.cell(0, 10, f"Algorithm used to sign {result['algorithm']}", 0, 1)
            self.ln(5)

    report = VerificationReport()
    report.add_page()
    for result in results:
        report.add_result(result)
    report.output(f"{filename[:-4]}_report.pdf")

