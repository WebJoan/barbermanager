import { useAuth } from '@hooks/useAuth';
import styles from './AdminSettings.module.scss';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';

function AdminSettings() {
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
            <div className={styles.description}>Manage your admin profile information</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="primary">
            Edit Profile
          </Button>
        </div>
      </Card>

      {/* System Settings */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="dashboard" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>System Settings</div>
            <div className={styles.description}>Configure system-wide settings</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Configure
          </Button>
        </div>
      </Card>

      {/* User Management */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="client" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>User Management</div>
            <div className={styles.description}>Manage barbers and clients</div>
          </div>
        </div>
        <div className={styles.actions}>
          <Button size="md" color="secondary">
            Manage Users
          </Button>
        </div>
      </Card>

      {/* Security Settings */}
      <Card className={styles.card}>
        <div className={styles.header}>
          <div className={styles.icon}>
            <Icon name="appointment" size="sm" black />
          </div>
          <div className={styles.content}>
            <div className={styles.title}>Security Settings</div>
            <div className={styles.description}>Password and security preferences</div>
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

export default AdminSettings;
