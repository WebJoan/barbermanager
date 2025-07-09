import { useAuth } from '@hooks/useAuth';
import styles from './BarberSettings.module.scss';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function BarberSettings() {
  const { profile } = useAuth();

  return (
    <>
      {/* Profile Settings */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="settings" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Profile Settings</div>
            <div className={styles.description}>Manage your barber profile information</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="primary">
            Edit Profile
          </Button>
        </div>
      </Card>

      {/* Services Settings */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="service" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Services & Pricing</div>
            <div className={styles.description}>Manage your services and pricing</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Manage Services
          </Button>
        </div>
      </Card>

      {/* Availability Settings */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="availability" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Availability</div>
            <div className={styles.description}>Set your working hours and availability</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Set Hours
          </Button>
        </div>
      </Card>

      {/* Notifications */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="appointment" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Notifications</div>
            <div className={styles.description}>Configure appointment and booking notifications</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Settings
          </Button>
        </div>
      </Card>
    </>
  );
}

export default BarberSettings;
