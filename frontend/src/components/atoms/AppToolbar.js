import { styled } from '@mui/material/styles';
import Toolbar from '@mui/material/Toolbar';

export default function AppToolbar() {

    const AppToolbar = styled(Toolbar)(({ theme }) => ({
        backgroundColor: "#899499",
        color: "white",
        fontWeight: "bold",
        height: "8vh"
    }));

    return (
        <AppToolbar>
            SYNCHRONY HUB
        </AppToolbar>
    )
}
