while true; do
    now=$(date +"%T")
    echo "Refreshing at ...$now"
    curl -X POST -H "Authorization: token $MASTER_KEY" \
        -H "Accept: application/vnd.github.everest-preview+json" \
        -d '{"ref": "main"}' \
        https://api.github.com/repos/sotnikola/sotex-stoni-rezervacije/actions/workflows/refresh.yaml/dispatches
    echo "Sleeping for 5 minutes..."
    sleep 300
done
