export const showError = (error, msg) => {
    return (
        <div className="container mt-3 alert alert-danger" style={{display: error ? '' : 'none'}}>
            {msg}
        </div>
    )
}

export const showSuccess = (success, msg) => {
    return (
        <div className="container mt-3 alert alert-success" style={{display: success ? '' : 'none'}}>
            {msg}
        </div>
    )
}

export const showLoading = (loading) => {
    return (
        <div className="container mt-3 alert alert-info" style={{display: loading ? '' : 'none'}}>
            Loading...
        </div>
    )
}