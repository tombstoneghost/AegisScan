import { Card, CardContent, CardHeader, Typography } from "@mui/material";

const Spider = ({results}) => {
    return (
        <div className="mt-4">
            <Card style={{height: '600px', overflowY: 'scroll'}}>
                <CardHeader title={<Typography variant="h5">Spider Results</Typography>} />
                <CardContent>
                    {String(results).split(",").map((res, i) => (
                        <div>
                            <Typography variant="p" key={i}>{res}</Typography>
                        </div>
                    ))}
                </CardContent>
            </Card>
        </div>
    )
};

export default Spider;