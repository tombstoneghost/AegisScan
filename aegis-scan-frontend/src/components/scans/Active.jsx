import { Card, CardContent, CardHeader, Chip, Typography } from "@mui/material";

const Active = ({results}) => {
    const getColor = (status) => {
        status = String(status).toLowerCase();

        if(status === 'informational') {
            return "info"
        } else if(status === 'low') {
            return 'success'
        } else if(status === 'medium') {
            return 'warning'
        } else if(status === 'high') {
            return 'error'
        }
    }
    

    return (
        <div className="mt-4">
            <Card style={{height: '600px', overflowY: 'scroll'}}>
                <CardHeader title={<Typography variant="h5">Active Results</Typography>} />
                <CardContent>
                    <div className="mb-2">
                        <Typography><strong>Total Alerts: </strong>{JSON.parse(results).length}</Typography>
                    </div>

                    {JSON.parse(results).map((alert, i) => (
                        <Card key={i} className="mb-4">
                            <CardContent>
                                <Typography><strong>Name: </strong>{alert.name}</Typography>
                                <Typography><strong>Target: </strong>{alert.url}</Typography>
                                <Typography><strong>Param: </strong>{alert.param}</Typography>
                                <div className=" mb-1 row">
                                    <div className="col">
                                        <Typography><strong>AI Prediction: </strong><Chip label={String(alert.ai_priority).charAt(0).toUpperCase() + String(alert.ai_priority).slice(1)} color={getColor(alert.ai_priority)}/> </Typography>
                                    </div>
                                    <div className="col">
                                        <Typography><strong>Risk: </strong><Chip label={alert.risk} color={getColor(alert.risk)}/> </Typography>
                                    </div>
                                    <div className="col">
                                        <Typography><strong>Confidence: </strong><Chip label={alert.confidence} color={getColor(alert.confidence)}/> </Typography>
                                    </div>
                                    <div className="col">
                                        <Typography><strong>Method: </strong><Chip label={alert.method} color="info"/> </Typography>
                                    </div>
                                </div>
                                <div className=" mt-1 row">
                                    <div className="col">
                                        <Typography><strong>Alert: </strong>{alert.alert}</Typography>
                                    </div>
                                    <div className="col">
                                        <Typography><strong>Plugin ID: </strong>{alert.pluginId}</Typography>
                                    </div>
                                    <div className="col">
                                        <Typography><strong>CWE ID: </strong>{alert.cweid}</Typography>
                                    </div>
                                </div>
                                <Typography><strong>Description: </strong>{alert.description}</Typography>
                                <Typography><strong>Solution: </strong>{alert.solution}</Typography>
                                <Typography><strong>Reference:</strong><a href={alert.reference} target="_blank">{alert.reference}</a></Typography>
                                <Typography><strong>Tags:</strong></Typography>
                                <div className="row">
                                    {Object.keys(alert.tags).map((t, i) => (
                                        <div className="col">
                                            <a href={alert.tags[t]} target="_blank"><Typography>{t}</Typography></a>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </CardContent>
            </Card>
        </div>
    )
};

export default Active;