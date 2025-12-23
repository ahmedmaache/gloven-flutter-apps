#!/bin/bash
# Script to generate all 100 Flutter apps

echo "Generating 100 Flutter apps..."

for i in {1..100}; do
    echo "Creating app $i/100..."
    ./scripts/create_app_template.sh $i
done

echo "All 100 apps generated successfully!"
echo "Total apps created: $(ls -1 apps/ | wc -l)"

