# pdf-highlight-remover
A simple Python script to remove highlights of a specific color (or color range) from a PDF file.

## Preliminaries

0. Make sure you have Python 3 installed. If not, go to the [official Python website](https://www.python.org/).

1. Clone this repo with `git clone https://github.com/cvee112/pdf-highlight-remover.git`

2. Change directory to the repo with `cd /path/to/repository` (Linux/macOS) or `cd C:\path\to\repository` (Windows)

3. Install dependencies with `pip install -r requirements.txt`

## Usage

1. Use a color picker like [Image Color Picker](https://imagecolorpicker.com/en) to get the RGB values of the highlight color you want to remove.
  
2. Try to estimate an appropriate range for each value. For best results, you will often need a range of values for R, G, and B.
   
3. Run the script with `python remove-highlights.py input_file_path output_file_path`

4. You will be prompted to input the RGB values (or range of values). Make sure to follow the specified format.

   For example:

   ```
   Input rgb value (or range in given format) to remove.

   r or [r_min, r_max]: [245, 255]
   g or [g_min, g_max]: [200, 240]
   b or [b_min, b_max]: [60, 210]
   ```

5. Check the results and iterate as needed. You may not get an adequate output the first time, but it will likely work with a refined range.

## Questions or feedback?

Feel free to contact me at [cvescobar112@protonmail.com](mailto:cvescobar112@protonmail.com).

## License

This work is licensed under the MIT License - see [LICENSE](LICENSE) for more details.
