#!/bin/bash
# Activate virtual environment
source /home4/astrohch/virtualenv/eos_simple_etc/3.11/bin/activate
export OPENBLAS_NUM_THREADS=1

# Assign a default port if $PORT is not set
PORT=${PORT:-8533}

# Output the port for debugging
echo "Using port: $PORT"

LOG_FILE=/home4/astrohch/signalcounts/streamlit_app.log

# Run the Python script to update .htaccess dynamically
#python /home4/astrohch/eos_simple_etc/update_htaccess.py >> $LOG_FILE

# Start the Streamlit app on the assigned port
streamlit run /home4/astrohch/signalcounts/myapp.py --server.port $PORT >> $LOG_FILE 2>&1
