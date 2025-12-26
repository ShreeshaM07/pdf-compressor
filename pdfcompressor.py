import streamlit as st
import subprocess
import os
import tempfile


def compress_pdf_aggressive(input_pdf, output_pdf, quality="ebook"):
    quality_map = {
        "screen": "/screen",
        "ebook": "/ebook",
        "printer": "/printer"
    }

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality_map[quality]}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]

    subprocess.run(cmd, check=True)


# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(page_title="PDF Compressor", layout="centered")

st.title("📄 PDF Compressor")
st.caption("High compression using Ghostscript (iLovePDF-style)")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

quality = st.selectbox(
    "Compression level",
    options=["screen", "ebook", "printer"],
    index=1,
    help="ebook = best balance (recommended)"
)

if uploaded_file is not None:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.pdf")
        output_path = os.path.join(tmpdir, "compressed.pdf")

        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Compress PDF"):
            with st.spinner("Compressing..."):
                compress_pdf_aggressive(
                    input_path,
                    output_path,
                    quality=quality
                )

            original_size = os.path.getsize(input_path) / 1024
            compressed_size = os.path.getsize(output_path) / 1024
            reduction = (1 - compressed_size / original_size) * 100

            st.success("Compression complete ✅")
            st.write(f"**Original size:** {original_size:.2f} KB")
            st.write(f"**Compressed size:** {compressed_size:.2f} KB")
            st.write(f"**Reduction:** {reduction:.2f}%")

            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇ Download compressed PDF",
                    data=f,
                    file_name="compressed.pdf",
                    mime="application/pdf"
                )
