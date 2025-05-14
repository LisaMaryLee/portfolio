# Apache Beam Dataflow example
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class CleanCSVLine(beam.DoFn):
    def process(self, element):
        fields = element.split(',')
        yield {
            'device_id': fields[0],
            'write_latency': float(fields[1]),
            'timestamp': fields[2]
        }

options = PipelineOptions(
    runner='DataflowRunner',
    project='your-gcp-project-id',
    region='us-central1',
    temp_location='gs://your-bucket/temp',
    staging_location='gs://your-bucket/staging',
    job_name='csv-transform-job'
)

with beam.Pipeline(options=options) as p:
    (p | 'Read CSV' >> beam.io.ReadFromText('gs://your-bucket/input.csv')
       | 'Parse CSV' >> beam.ParDo(CleanCSVLine())
       | 'Write JSONL' >> beam.io.WriteToText('gs://your-bucket/output/output', file_name_suffix='.json'))
