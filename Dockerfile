FROM continuumio/miniconda3:latest

RUN conda create -n images python=3.12.1 -y
RUN echo "source activate images" > ~/.bashrc
ENV PATH /opt/conda/envs/images/bin:$PATH

COPY . .

RUN pip install -r requirements.txt

SHELL ["conda", "run", "--name", "images", "/bin/bash", "-c"]

EXPOSE 80

CMD ["conda", "run", "--name", "images", "uvicorn", "model.train:app", "--host", "0.0.0.0", "--port", "80"]