while true; do
    curl -X POST -H "Authorization: token $MASTER_KEY" \
        -H "Accept: application/vnd.github.everest-preview+json" \
        -d '{"ref": "main"}' \
        https://api.github.com/repos/sotnikola/sotex-stoni-rezervacije/actions/workflows/refresh.yaml/dispatches

    sleep 180
done
