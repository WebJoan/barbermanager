import { useAuth } from '@hooks/useAuth';
import styles from './ClientSettings.module.scss';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function ClientSettings() {
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
            <div className={styles.description}>Manage your personal information</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="primary">
            Edit Profile
          </Button>
        </div>
      </Card>

      {/* Appointment Preferences */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="appointment" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Appointment Preferences</div>
            <div className={styles.description}>Set your preferred booking times and barbers</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Preferences
          </Button>
        </div>
      </Card>

      {/* Notifications */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="calendar" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Notifications</div>
            <div className={styles.description}>Configure appointment reminders and updates</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Settings
          </Button>
        </div>
      </Card>

      {/* Privacy & Security */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="client" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Privacy & Security</div>
            <div className={styles.description}>Password and privacy settings</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Security
          </Button>
        </div>
      </Card>
    </>
  );
}

export default ClientSettings;
