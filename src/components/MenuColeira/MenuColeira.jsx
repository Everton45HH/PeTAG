import * as React from 'react';
import { styled } from '@mui/material/styles';
import SpeedDial from '@mui/material/SpeedDial';
import SpeedDialIcon from '@mui/material/SpeedDialIcon';
import SpeedDialAction from '@mui/material/SpeedDialAction';

import MenuIcon from '@mui/icons-material/Menu';
import AddIcon from '@mui/icons-material/Add';
import PetsIcon from '@mui/icons-material/Pets';
import CloseIcon from '@mui/icons-material/Close';

const StyledSpeedDial = styled(SpeedDial)(({ theme }) => ({
  position: 'fixed',    
  bottom: theme.spacing(3),
  right: theme.spacing(3),
  zIndex: 1300,         
}));

export default function MenuColeira({ onAddCollar, onSimulate }) {
  return (
    <StyledSpeedDial
      ariaLabel="Menu de coleiras"
      icon={<SpeedDialIcon icon={<MenuIcon />} openIcon={<CloseIcon />} />}
      direction="left"
    >
      <SpeedDialAction
        icon={<AddIcon />}
        tooltipTitle="Criar coleira"
        onClick={onAddCollar}
      />

      <SpeedDialAction
        icon={<PetsIcon />}
        tooltipTitle="Modo simulação"
        onClick={onSimulate}
      />
    </StyledSpeedDial>
  );
}