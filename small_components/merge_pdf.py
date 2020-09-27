def merge_pdf(folder, fout=None, pdf_filter=None, sort_key=None, reversed=False, 
    overwrite=False):

    """
    pdf_filter: a criterion that test if a file is PDF
    """
    def is_valid_pdf(name):
        try:
            with open(name, 'rb') as fin:
                PdfFileReader(fin)
        except:
            return False
        else:
            return True

    def _pdf_filter(file):
        if pdf_filter is None:
            return True
        else:
            return pdf_filter(file)

    import os
    from PyPDF2 import PdfFileMerger, PdfFileReader
    import PyPDF2
    all_pdf_files = list(filter(lambda file: is_valid_pdf(file),
                           [os.path.join(folder, file) for file in os.listdir(folder)]))

    pdf_files_to_merge = [os.path.join(folder, file)
                          for file in os.listdir(folder) if _pdf_filter(file)]
    pdf_files_to_merge = list(
        filter(lambda file: is_valid_pdf(file), pdf_files_to_merge))
    pdf_files_to_merge = sorted(pdf_files_to_merge, key=sort_key, reverse=reversed)
    merger = PdfFileMerger(strict=False)
    for file in pdf_files_to_merge:
        try:
            merger.append(open(file, 'rb'))
            print('name', file)
        except Exception as e:
            print('wrong', e)
    # if fout is None, set fout to "folder.pdf"
    # at the same time, avoid name clash
    if fout is None:
        fout = os.path.join(folder, str(os.path.basename(folder)) + '.pdf')
        original_fout = fout 
        found_name = False
        while not found_name:
            if overwrite:
                break 
            if fout in all_pdf_files:
                number_of_iterate = 100000
                for i in range(1, number_of_iterate):
                    fout = original_fout.split('.')[0] + str(i) + ".pdf"
                    if fout not in all_pdf_files:
                        found_name = True
                        break
            else:
                found_name = True

    with open(fout, 'wb') as fout:
        merger.write(fout)







