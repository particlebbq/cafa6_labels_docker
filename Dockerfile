FROM python:3
WORKDIR /work

COPY requirements.txt /work/requirements.txt
RUN pip install -r requirements.txt

COPY collect_testsuperset_ids.py /work/collect_testsuperset_ids.py
COPY compare_label_sets.py /work/compare_label_sets.py
COPY run_all.sh /work/run_all.sh

CMD ["/work/run_all.sh"]

