import { Card, CardContent, CardHeader, Divider, Typography } from "@mui/material";

const Spider = ({results}) => {
    return (
        <div className="mt-4">
            <Card style={{height: '600px', overflowY: 'scroll'}}>
                <CardHeader title={<Typography variant="h5">Spider Results</Typography>} />
                <CardContent>
                    {JSON.parse(results).map((alert, i) => (
                        <div key={i}>
                            <Typography>URL: {String(alert.requestHeader).split(" ")[1]}</Typography>
                            <Divider />
                        </div>
                    ))}
                </CardContent>
            </Card>
        </div>
    )
};

export default Spider;